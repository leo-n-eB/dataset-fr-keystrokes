splitter_strokes = "\u001d"
splitter_infos = "\u001f"
deleting_marker = "\u0000"
insertion_marker = "\u0002"

ponctuation = [",", ";", ":", "!", "?", ".", "/", "(", ")", "'", "...", " "]


def decoding(all_texts, text_type, student_id, exercise_id, keystrokes):
    final_text = all_texts[1]
    context = all_texts[0]
    if len(all_texts) == 3:
        context += all_texts[2]
    keystrokes = keystrokes.split(splitter_strokes)

    text_list = [keystrokes[0][0]]  # we initialise with the first character
    time_list = [int(keystrokes[0][2:])]  # we initialise with the first timestmap
    cursor_list = [1]
    i = 1
    shift = 0  # to handle the corrector's shift on cursors
    while i < len(keystrokes):
        if i < len(keystrokes) - 1:
            next_stroke = keystrokes[i + 1]
            next_stroke = next_stroke.split(splitter_infos)
        stroke = keystrokes[i]
        stroke = stroke.split(splitter_infos)
        prev_text = text_list[i - 1]

        match stroke[0], len(stroke):
            #  insertion
            case "\u0002", _:

                # parsing
                new_char = stroke[2]
                cursor = int(stroke[1])
                new_text = prev_text[:cursor] + new_char + prev_text[cursor:]

                # storing
                text_list.append(new_text)
                cursor_list.append(cursor + 1)
                time_list.append(time_list[i - 1] + int(stroke[3]))
                i += 1

            # deletion last char
            case "\u0000", 2:
                # parsing
                new_text = prev_text[:-1]
                # storing
                text_list.append(new_text)
                cursor_list.append(len(prev_text) - 1)
                time_list.append(time_list[i - 1] + int(stroke[1]))
                i += 1

            # deletion
            case "\u0000", _:
                if next_stroke[0] == insertion_marker and len(next_stroke[2]) > 1:
                    cursor = int(stroke[1])

                    cur_start = find_start_prev_word(prev_text, cursor - 1)
                    cur_end = find_end_word(prev_text, cursor)
                    new_text = prev_text[:cur_start] + prev_text[cur_end:]
                    text_list.append(new_text)
                    cursor_list.append(cursor)
                    time_list.append(time_list[i - 1] + int(stroke[3]))
                    i += 1
                    new_text = (
                        prev_text[:cur_start] + next_stroke[2] + prev_text[cur_end:]
                    )
                    text_list.append(new_text)
                    cursor_list.append(cur_start + len(next_stroke[2]))
                    time_list.append(time_list[i - 1] + int(next_stroke[3]))
                    i += 1
                elif (
                    next_stroke[0] not in [deleting_marker, insertion_marker]
                    and len(next_stroke) == 2
                    and len(next_stroke[0]) > 1
                ):
                    cursor = int(stroke[1])
                    cur_start = find_start_prev_word(prev_text, cursor - 1)
                    cur_end = find_end_word(prev_text, cursor)
                    new_text = prev_text[:cur_start]
                    text_list.append(new_text)
                    cursor_list.append(cur_start)
                    time_list.append(time_list[i - 1] + int(stroke[3]))
                    i += 1
                    new_text = prev_text[:cur_start] + next_stroke[0]

                    text_list.append(new_text)
                    cursor_list.append(cur_start + len(next_stroke[0]))
                    time_list.append(time_list[i - 1] + int(next_stroke[1]))
                    i += 1

                else:
                    if int(stroke[2]) == int(stroke[1]):
                        stroke[2] = str(int(stroke[2]) + 1)

                    elif int(stroke[2]) < int(stroke[1]):
                        stroke[1], stroke[2] = stroke[2], stroke[1]
                    new_text = prev_text[: int(stroke[1])] + prev_text[int(stroke[2]) :]
                    text_list.append(new_text)
                    cursor_list.append(int(stroke[1]))
                    time_list.append(time_list[i - 1] + int(stroke[3]))
                    i += 1

            # simple adding at the end
            case _, _:
                text_list.append(prev_text + stroke[0])
                cursor_list.append(len(prev_text + stroke[0]))
                time_list.append(time_list[i - 1] + int(stroke[1]))

                i += 1

    decoded_data = dict()
    decoded_data["final_text"] = final_text
    decoded_data["context"] = context
    decoded_data["text_type"] = text_type
    decoded_data["time_list"] = time_list
    decoded_data["text_list"] = text_list
    decoded_data["cursor_list"] = cursor_list
    decoded_data["student_id"] = student_id
    decoded_data["exercise_id"] = exercise_id
    return decoded_data


def find_start_prev_word(prev_text: str, cursor: int) -> int:
    found = False
    cur = cursor

    if cursor >= len(prev_text):
        cur = len(prev_text) - 1

    while not found and cur > 0:
        if prev_text[cur] == " " or prev_text[cur] in ponctuation:
            found = True
        else:
            cur -= 1
    return cur + 1


def find_end_word(prev_text: str, cursor: int) -> int:
    found = False
    cur = cursor
    if cursor >= len(prev_text):
        cur = len(prev_text) - 1
    while not found and cur < len(prev_text):
        if prev_text[cur] == " " or prev_text[cur] in [
            ",",
            ";",
            ":",
            "!",
            "?",
            ".",
            "/",
            "(",
            ")",
            "...",
        ]:
            found = True
        else:
            cur += 1
    return cur
