# %%
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()
DUMP = True if os.getenv("DUMP_MESSAGES") == 'True' else False
WORK_DIRECTORY = os.getcwd()


def process_whatsapp_message(message: str, corresponded: str) -> str:
    """Process a WhatsApp message
    Args:
        message (str): Message to be processed
        corresponded (str): Corresponded of the bot

    Returns:
        str: Processed message
    """

    return message.lower().replace(f'{corresponded} ', '')


def process_whatsapp_chat(input_file_path: str, output_file_path: str) -> None:
    """Process a WhatsApp chat exported as a CSV file from the WhatsApp app
    Args:
        input_file_path (str): Path to the input CSV file
        output_file_path (str): Path to the output JSON file

    Returns:
        None
    """
    stamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data = pd.read_csv(input_file_path, sep=';', encoding='utf-8', header=0)

    data['timestamp'] = data['from'].str.extract(r'^\[(.*?)\]')
    data['phone_number'] = data['from'].str.extract(r'\](.*?)\:')
    data.drop(columns=['from'], inplace=True)

    data['timestamp'] = data['timestamp'].str.strip()
    data['phone_number'] = data['phone_number'].str.strip()

    sub_data = data[['name', 'phone_number']].drop_duplicates()
    sub_data.loc[~sub_data['phone_number'].str.startswith(
        '+'), 'name'] = sub_data['phone_number']
    sub_data = sub_data.dropna(subset=['name']).drop_duplicates()
    sub_data.dropna(subset=['phone_number'], inplace=True)

    data['name'] = data['phone_number'].replace(
        sub_data.set_index('phone_number')['name'])
    data.drop(columns=['phone_number'], inplace=True)
    data.dropna(subset=['name'], inplace=True)
    try:
        subdata = data['reply'].str.split('\t', n=2, expand=True)
        if subdata.shape[1] == 3:
            subdata_names = subdata[[0, 1]].drop_duplicates().dropna()

            data['name'] = data['name'].replace(
                subdata_names.set_index(1)[0])

            data['reply'] = subdata[0] + ": " + subdata[2]
    except AttributeError:
        pass
    data['timestamp'] = data['timestamp'].str.replace(',', ' no dia')
    data_final_content = []
    for index, row in data.iterrows():
        if str(row['reply']) == 'nan':
            data_final_content.append(
                f"{row['name']}: {row['message']}")
            continue
        data_final_content.append(
            f"{row['name']}: {row['message']} respondendo {row['reply']}")

    data_final = pd.DataFrame(
        data_final_content, columns=['content'])
    data_final['role'] = 'user'
    data_final = data_final[['role', 'content']]

    data = data.reindex(columns=['name', 'message', 'reply', 'timestamp'])
    if not Path.exists(Path(f"{WORK_DIRECTORY}/data/messages/dump_messages")):
        Path.mkdir(Path(f"{WORK_DIRECTORY}/data/messages/dump_messages"))
    if DUMP:
        data.to_csv(Path(f"{WORK_DIRECTORY}/data/messages/dump_messages/{stamp}.csv"),
                    sep=';', encoding='utf-8', index=False)
    data_final.to_json(output_file_path, orient='records')
# %%

# %%
