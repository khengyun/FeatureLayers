import re
import fileinput
import subprocess
from featurelayers.__version__ import __version__
from rich import print


def git_add_commit_push(commit_message):
    try:
        # Add all files to staging area
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push to remote repository
        subprocess.run(["git", "push"], check=True)

        print("[bold green]Push successful![/bold green]")
    except subprocess.CalledProcessError as e:
        print(f"[bold red]Error: {e}[/bold red]")


# Đọc giá trị version từ module featurelayers

version = __version__

# Tách version thành các phần tử số
version_parts = list(map(int, version.split('.')))

# Tăng giá trị cuối cùng lên 1
version_parts[-1] += 1

# Kiểm tra và điều chỉnh giá trị các phần tử
for i in range(len(version_parts) - 1, 0, -1):
    if version_parts[i] > 9:
        version_parts[i] = 0
        version_parts[i - 1] += 1

# Chuyển đổi lại thành chuỗi và gắn giá trị version mới
new_version = '.'.join(map(str, version_parts))
new_version_str = f'"{new_version}"'

# Lưu giá trị version vào file __version__
with fileinput.FileInput('./featurelayers/__version__.py', inplace=True) as file:
    for line in file:
        line = re.sub(r'__version__ = .*', f'__version__ = {new_version_str}', line.rstrip())
        print(line)

# Nhập nội dung commit từ người dùng
commit_message = input("Enter Commit Content: ")

# Gắn giá trị version vào nội dung commit
commit_message_with_version = f"{commit_message} (Version {new_version})"

# Thực hiện add, commit và push với commit_message_with_version
git_add_commit_push(commit_message_with_version)
