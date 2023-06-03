# %%
import pandas as pd
import os


def process_whatsapp_message(message: str, corresponded: str) -> str:

    return message.lower().replace(f'{corresponded} ', '')


def process_whatsapp_chat(input_file_path: str, output_file_path: str) -> None:
    """Process a WhatsApp chat exported as a CSV file from the WhatsApp app
    Args:
        input_file_path (str): Path to the input CSV file
        output_file_path (str): Path to the output CSV file

    Returns:
        None
    """
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

    subdata = data['message'].str.split('\t', n=2, expand=True)
    if len(subdata.columns.tolist()) > 1:
        subdata[2] = subdata.apply(lambda row: f"""{row[1]}\t{row[2] if row[2] is not None else ''}""" if row[1]
                                   is not None and not row[1].startswith('+') else row[2], axis=1)
        subdata.drop(columns=[1], inplace=True)

        msgs = subdata.apply(
            lambda row: row[0] if row[2] is None else None, axis=1)
    else:
        msgs = subdata.apply(lambda row: row[0], axis=1)
    for i, msg in enumerate(msgs):
        if msg is None:
            plain_msg = subdata.iloc[i, -1].split('\t')
            plain_msg_strip = [s.strip() for s in plain_msg]
            msgs[
                i] = f""" respondendo: {plain_msg_strip[-1]}. Para {subdata.iloc[i, 0]} sobre a seguinte mensagem: {' '.join(plain_msg_strip[:-1])}."""
        else:
            msgs[i] = f": {msg}"
    data.drop(columns=['message'], inplace=True)
    data['message'] = msgs

    data['timestamp'] = data['timestamp'].str.replace(',', ' no dia')
    data_final = data.apply(
        lambda row: f"{row['name']}{row['message']}", axis=1)
    data = data.reindex(columns=['name', 'message', 'timestamp'])
    data.to_csv(f"{os.getcwd()}\\data\\messages\\messages_extracted.csv",
                sep=';', encoding='utf-8', index=False)
    data_final.to_csv(output_file_path, sep=';',
                      encoding='utf-8', index=False, header=False)
