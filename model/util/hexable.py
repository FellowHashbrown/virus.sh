import os
from json import dumps, loads


class Hexable:

    @staticmethod
    def save(json: dict, file: str):

        # Convert the JSON object into a list of hex bytes
        result = []
        for char in dumps(json):
            result.append(hex(ord(char))[2:])

        # Save the file separating each line of hex bytes into 16
        with open(file, "w") as save_file:
            total_processed = 0
            for hex_byte in result:
                save_file.write(hex_byte + " ")
                total_processed += 1
                if total_processed % 16 == 0:
                    save_file.write("\n")

    @staticmethod
    def load(file: str) -> dict:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File, {file} does not exist")

        with open(file) as save_file:
            hex_data = "".join(save_file.readlines()).strip().split(" ")

        # Convert the list of hex data bytes back into JSON
        save_json = ""
        for hex_byte in hex_data:
            save_json += chr(int(hex_byte, 16))
        return loads(save_json)