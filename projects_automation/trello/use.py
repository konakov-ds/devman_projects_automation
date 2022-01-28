import logging
import os
from dotenv import load_dotenv
from trello import create_workspace, create_board, add_members_board

groups = [
    {
        'pm_name': 'Тим',
        'start_from': '18:00',
        'board_bg': 'green',
        'students': [
            {'name': 'Марк', 'email': 'box1@mail.org'},
            {'name': 'Никита', 'email': 'box2@mail.org'},
            {'name': 'Евгений', 'email': 'box3@mail.org'}
            ]
    },
    {
        'pm_name': 'Тим',
        'start_from': '19:00',
        'board_bg': 'green',
        'students': [
            {'name': 'Иван', 'email': 'box11@mail.org'},
            {'name': 'Семён', 'email': 'box12@mail.org'},
            {'name': 'Елена', 'email': 'box13@mail.org'}
            ]

    },
    {
        'pm_name': 'Катя',
        'start_from': '19:00',
        'board_bg': 'blue',
        'students': [
            {'name': 'Игорь', 'email': 'box21@mail.org'},
            {'name': 'Егор', 'email': 'box22@mail.org'},
            {'name': 'Иван', 'email': 'box23@mail.org'}
            ]
    },
    {
        'pm_name': 'Илья',
        'start_from': '19:30',
        'board_bg': 'red',
        'students': [
            {'name': 'Артём', 'email': 'box31@mail.org'},
            {'name': 'Анна', 'email': 'box32@mail.org'},
            {'name': 'Василий', 'email': 'box33@mail.org'}
            ]
    }
]


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
    2.1 Добавление в memebers доски email студентов
    """    
    for group in groups:
        board_name = f'{group["start_from"]} {", ".join([student["name"] for student in group["students"]])}'
        board_id, board_url = create_board(
                trello_apikey,
                trello_token,
                wrksp_id,
                board_name,
                group['board_bg']
                )
        
        for student in group['students']:
            add_members_board(trello_apikey, trello_token, board_id, student['email'])
            print(f'Направить ссылку {board_url} студенту {student["name"]} - {student["email"]}')
        # ToDo как дружить с django моделями? 


if __name__ == '__main__':
    main()