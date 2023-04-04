import pdb

DELIMITER = '\n'
MAX_BYTE = 1024 * 13  # 15k
UNICODE = 'utf-8'



def wrap_text(texts):
    """
    번역을 하지 않는 구간을 특정 기호로 문장을 합쳐서 요청한다.
    예) ['안녕하세요', '밥 먹었습니까?'] → '안녕하세요\n밥 먹었습니까?'
    """
    texts = [text.replace(DELIMITER, '<span class="notranslate">space</span>') for text in texts]
    return DELIMITER.join(texts)

def unwrap_text(wrapped_text):
    """
    번역된 문장을 다시 특정 기호로 문장을 잘라준다.
    예) '안녕하세요\n밥 먹었습니까?' →  ['안녕하세요', '밥 먹었습니까?']
    """
    texts = wrapped_text.split(DELIMITER)
    texts = [text.replace('<span class="notranslate">space</span>', DELIMITER) for text in texts]
    return texts
    
def chunk_text_byte(text, max_byte=MAX_BYTE, delimiter=DELIMITER):
    """
    대량의 번역 문장들을 순차적으로 translate 함수를 요청시 내부적으로는 API 요청을 여러번 요청하게 되어 있으므로 성능적으로 느린 응답을 가져오게 된다.
    15K 까지 글자수가 제한이 되어있으므로 15K씩 잘라서 요청하는 것으로 네트워크 부하를 줄일 수 있다.
    """
    text = text.encode(UNICODE)
    delimiter = delimiter.encode(UNICODE)
    words = iter(text.split(delimiter))
    lines, current = [], next(words)


    for word in words:
        if len(current) + 1 + len(word) > max_byte:
            lines.append(current.decode(UNICODE))
            current = word
        else:
            current += delimiter + word
    lines.append(current.decode(UNICODE))
    return lines