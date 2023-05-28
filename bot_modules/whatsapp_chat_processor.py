import pandas as pd


def process_whatsapp_chat(input_file_path, output_file_path) -> None:
    """Process a WhatsApp chat exported as a CSV file from the WhatsApp app
    Args:
        input_file_path (str): Path to the input CSV file
        output_file_path (str): Path to the output CSV file

    Returns:
        None
    """
    # Read the input CSV file into a DataFrame
    data = pd.read_csv(input_file_path, sep=';', encoding='utf-8', header=0)

    # Extract the timestamp and phone number from the 'from' column
    data['timestamp'] = data['from'].str.extract(r'^\[(.*?)\]')
    data['phone_number'] = data['from'].str.extract(r'(\+\d.*?):')
    data.drop(columns=['from'], inplace=True)

    # Extract the name from the phone number and drop duplicates
    sub_data = data.dropna(subset=['phone_number'])[
        ['name', 'phone_number']].drop_duplicates()
    sub_data.dropna(subset=['name'], inplace=True)
    data['name'] = data['phone_number'].replace(
        sub_data.set_index('phone_number')['name'])
    data.drop(columns=['phone_number'], inplace=True)

    # Split the message column into two columns and format the messages
    subdata = data['message'].str.split('\t', n=2, expand=True)
    subdata.drop(columns=[1], inplace=True)
    msgs = subdata.apply(
        lambda row: row[0] if row[2] is None else None, axis=1)
    for i, msg in enumerate(msgs):
        if msg is None:
            plain_msg = subdata.iloc[i, -1].split('\t')
            plain_msg_strip = [s.strip() for s in plain_msg]
            msgs[
                i] = f""" respondendo: {plain_msg_strip[-1]} para {subdata.iloc[i, 0]} sobre a seguinte mensagem: {' '.join(plain_msg_strip[:-1])}"""
        else:
            msgs[i] = f": {msg}"
    data.drop(columns=['message'], inplace=True)
    data['message'] = msgs

    # Format the timestamp and concatenate the columns into a final message column
    data['timestamp'] = data['timestamp'].str.replace(',', ' no dia')
    data['final_message'] = data.apply(
        lambda row: f"Mensagem de {row['name']}{row['message']} as {row['timestamp']}", axis=1)
    data.drop(columns=['name', 'timestamp', 'message'], inplace=True)

    # Write the processed data to the output CSV file
    data.to_csv(output_file_path, sep=';',
                encoding='utf-8', index=False, header=False)


# %%
process_whatsapp_chat(r"C:\Projetos\Chat Bot Whatsapp\data\messages\messages_extracted.csv",
                      r"C:\Projetos\Chat Bot Whatsapp\data\messages\messages_extracted_processed.csv")
