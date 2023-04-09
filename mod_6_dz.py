from pathlib import Path
import shutil
import re
import sys

folders = []
images = []
video = []
documents = []
audio = []
archives = []
unknown = []
unknown_extensions = set()
known_extensions = set()


def files_finder(path: Path):
    '''пошук всіх файлів та папок в заданому шляху'''

    for element in path.iterdir():
        if element.is_dir():
            if element.name not in ('images', 'audio', 'video', 'documents', 'archives'):
                folders.append(element)
                files_finder(element)
        else:
            file_mover(element)


file_manager = {
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'odt', 'xls'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'archives': ['zip', 'gz', 'tar'],
    'unknown': []
    }


def file_mover(file: Path) -> None:
    is_file_copy = False
    file_extension = file.suffix[1:]
    file_extension_normalized = file.suffix
    file_name = normalize(file.name.removesuffix(file_extension_normalized))
    file_name_good = file_name + file_extension_normalized

    for key, value in file_manager.items():
        for extension in value: # пошук розширення в значеннях словника
            if file_extension.lower() == extension:
                known_extensions.add(file_extension)
                new_dir = output_dir / key
                new_dir.mkdir(exist_ok=True, parents=True)
                if file_extension in file_manager['archives']:
                    archive_name = normalize(str(file.name.removesuffix('.zip' or '.tar' or '.gz')))
                    archive_dir = output_dir / key / archive_name
                    archive_dir.mkdir(exist_ok=True, parents=True)
                    archive_extractor(file, archive_dir)
                    is_file_copy = True
                else:
                    file.replace(new_dir / file_name_good)
                    is_file_copy = True


                # запис скопійованих файлів у відповідні списки

                if key == 'images':
                    images.append(file.name)
                elif key == 'video':
                    video.append(file.name)
                elif key == 'documents':
                    documents.append(file.name)
                elif key == 'audio':
                    audio.append(file.name)
                elif key == 'archives':
                    archives.append(file.name)
                elif key == 'unknown':
                    unknown.append(file.name)

    if not is_file_copy: # якщо невідоме розширення, то:
        unknown_extensions.add(file_extension)
        # file_manager['unknown'].append(file_extension)
        new_dir = output_dir / 'unknown'
        new_dir.mkdir(exist_ok=True)
        # print(f'coping a file: {file.name} to {new_dir}')
        file.replace(new_dir / file_name_good)
        unknown.append(file.name)


def copied_files() -> None:
    if len(images) > 0:
        print(f'sorted files to category "images": ')
        print('*' * 30)
        for file in images:
            print(file)
    if len(video) > 0:
        print(f'sorted files to category "video": ')
        print('*' * 30)
        for file in video:
            print(file)
    if len(documents) > 0:
        print(f'sorted files to category "documents": ')
        print('*' * 30)
        for file in documents:
            print(file)
    if len(audio) > 0:
        print(f'sorted files to category "audio": ')
        print('*' * 30)
        for file in audio:
            print(file)
    if len(archives) > 0:
        print(f'sorted files to category "archives": ')
        print('*' * 30)
        for file in archives:
            print(file)
    if len(unknown) > 0:
        print(f'sorted files to category "unknown": ')
        print('*' * 30)
        for file in unknown:
            print(file)


def archive_extractor(file: Path, path: Path):
    try:
        shutil.unpack_archive(file, path)
    except shutil.ReadError:
        print(f'Cannot unpack archive {file.name}')
    else:
        file.unlink()

    return


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(file_name: str) -> str:
    normalized_name = file_name.translate(TRANS)
    normalized_name = re.sub(r'\W', '_', normalized_name)

    return normalized_name


def delete_folder() -> None:
    for folder in folders:
        try:
            folder.rmdir()
        except OSError:
            print(f'Folder {folder} can not be deleted')


if __name__ == '__main__':
    # path = Path('for_test')
    path = Path(sys.argv[1])
    output_dir = path
    files_finder(path)
    copied_files()
    delete_folder()
    print(f'sorted known_extensions is: {known_extensions}')
    print(f'sorted unknown_extensions is: {unknown_extensions}')


