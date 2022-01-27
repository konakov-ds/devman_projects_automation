import logging
import os
from dotenv import load_dotenv
from trello import create_workspace, create_board


def main():
    load_dotenv()
    trello_apikey = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")

    """
    1. Создание рабочего пространства workspace/organization
    Проект {project_name} [{project_start_date}-{project_end_date}]
    """
    wrksp_name='Проект "DEVMAN" [10.02.2022 - 17.02.2022]'
    wrksp_id = create_workspace(
            trello_apikey,
            trello_token,
            wrksp_name=wrksp_name
            )

    """
    2. Создание внутри рабочего пространства(проекта) групп(досок) команд
    """    
    groups = [
        {
            'pm_name': 'Тим',
            'start_from': '18:00',
            'board_bg': 'green',
            'students': ['Марк', 'Никита', 'Евгений']
        },
        {
            'pm_name': 'Тим',
            'start_from': '19:00',
            'board_bg': 'green',
            'students': ['Иван', 'Семён', 'Елена']
        },
        {
            'pm_name': 'Катя',
            'start_from': '19:00',
            'board_bg': 'blue',
            'students': ['Игорь', 'Егор', 'Иван']
        },
        {
            'pm_name': 'Илья',
            'start_from': '19:30',
            'board_bg': 'red',
            'students': ['Артём', 'Анна', 'Василий']
        }
    ]
    for group in groups:
        board_name = f'{group["start_from"]} {", ".join(group["students"])}'
        board_url = create_board(
            trello_apikey,
            trello_token,
            wrksp_id,
            board_name,
            group['board_bg']
            )
        print(f'Направить ссылку {board_url} студентам {group["students"]}')
        # ToDo?


if __name__ == '__main__':
    main()