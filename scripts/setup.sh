#!/bin/bash

set -euo pipefail

# プロジェクトのルートディレクトリを取得
project_root_dir=$(cd $(dirname $0)/.. && pwd)

# プロジェクトのルートディレクトリに移動
cd $project_root_dir


# 仮想環境のチェック
check_venv() {
    echo "=== VIRTUAL_ENV環境変数チェック ==="
    if [ -n "${VIRTUAL_ENV:-}" ]; then
        echo "✅ 仮想環境がアクティブです: $VIRTUAL_ENV"
        return 0
    else
        echo "❌ 仮想環境がアクティブではありません"
        return 1
    fi
}

# pythonのパスをチェック
check_python_path() {
    echo "=== Pythonのパスチェック ==="
    if ! command -v python >/dev/null 2>&1; then
        echo "❌ pythonコマンドが見つかりません"
        return 1
    fi

    python_path=$(which python)

    if [[ "$python_path" == *"/venv/"* ]] || [[ "$python_path" == *"/$project_root_dir/"* ]]; then
        echo "✅ 仮想環境のPythonを使用中: $python_path"
        return 0
    else
        echo "❌ システムのPythonを使用中: $python_path"
        return 1
    fi
}

# pipのパスをチェック
check_pip_path() {
    echo "=== pipのパスチェック ==="
    if ! command -v pip >/dev/null 2>&1; then
        echo "❌ pipが見つかりません"
        return 1
    fi

    pip_path=$(which pip)
    if [[ "$pip_path" == *"/venv/"* ]] || [[ "$pip_path" == *"/$project_root_dir/"* ]]; then
        echo "✅ 仮想環境のpipを使用中: $pip_path"
        return 0
    else
        echo "❌ システムのpipを使用中: $pip_path"
        return 1
    fi
}

# 環境チェック
check_env() {
    if ! check_venv; then return 1; fi
    echo
    if ! check_python_path; then return 1; fi
    echo
    if ! check_pip_path; then return 1; fi
    echo
    return 0
}

# 仮想環境のアクティベート
activate_venv() {
    if ! [ -d venv ]; then
        return 1
    fi

    if ! [ -f venv/bin/activate ]; then
        return 1
    fi

    if ! source venv/bin/activate; then
        return 1
    fi

    if ! check_env; then
        return 1
    fi

    return 0
}

# 仮想環境の作成とアクティベート
create_venv() {
    echo "=== 仮想環境の作成 ==="

    if [ -d venv ]; then
        echo "既存のvenvを削除中..."
        rm -rf venv
    fi

    echo "新しい仮想環境を作成中..."
    if ! python3 -m venv venv; then
        echo "❌ 仮想環境の作成に失敗しました"
        exit 1
    fi

    echo "仮想環境をアクティベート中..."
    if ! activate_venv; then
        echo "❌ 仮想環境のアクティベートに失敗しました"
        exit 1
    fi

    echo "✅ venvが正常に作成・アクティベートされました"
}

# 依存関係のインストール
install_dependencies() {
    echo "=== 依存関係のインストール ==="

    if [ ! -f requirements.txt ]; then
        echo "❌ requirements.txtが見つかりません"
        exit 1
    fi

    if ! pip install -r requirements.txt; then
        echo "❌ 依存関係のインストールに失敗しました"
        exit 1
    fi

    echo "✅ 依存関係が正常にインストールされました"
}

main() {
    is_already_activated=false

    echo "🚀 セットアップを開始します"
    echo

    if check_env; then
        echo "✅ 環境チェックに成功しました"
        echo
        is_already_activated=true
    else
        if ! activate_venv; then
            echo
            create_venv
        fi
    fi

    install_dependencies
    echo

    if ! $is_already_activated; then
        echo "venvのアクティベートは以下のコマンドで行えます"
        echo "source venv/bin/activate"
    fi
}

main