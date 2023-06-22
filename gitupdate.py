import re
import fileinput
import subprocess
from featurelayers.__version__ import __version__
import git
from rich import print
from pathlib import Path


def git_add_commit_push(message):
    try:
        # Add all files to staging area
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", message], check=True)

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
commit_message_with_version = f"{commit_message} (Version {new_version_str})"



# Cập nhật nội dung trong README với phiên bản mới nhất
repo = git.Repo()
readme_file = 'README.md'
readme = Path(repo.working_dir) / readme_file

# Đọc nội dung README
with open(readme, 'r') as f:
    content = f.read()

# Kiểm tra sự tồn tại của __version__
if '__version__' not in content:
    # Thêm __version__ vào nội dung README
    new_content = content + f'\n__version__ = "{new_version_str}"\n'
else:
    # Tìm và thay thế phiên bản cũ trong README bằng phiên bản mới
    new_content = re.sub(r'__version__ = .*', f'__version__ = "{new_version_str}"', content)

# Ghi nội dung mới vào README
with open(readme, 'w') as f:
    f.write(new_content)
# Thực hiện add, commit và push với commit_message_with_version
git_add_commit_push(commit_message_with_version)
print("[bold green]README updated with the latest version![/bold green]")
