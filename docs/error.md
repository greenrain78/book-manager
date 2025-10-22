
### 입력시 백스페이스바

ID를 입력하세 asfasf       
--- Logging error ---
Traceback (most recent call last):
  File "/usr/lib/python3.12/logging/__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
UnicodeEncodeError: 'utf-8' codec can't encode characters in position 59-60: surrogates not allowed
Call stack:
  File "/mnt/c/Users/kdwkd/PycharmProjects/book-manager/main.py", line 22, in <module>
    main_prompt(app=app)
  File "/mnt/c/Users/kdwkd/PycharmProjects/book-manager/src/prompt/start.py", line 60, in main_prompt
    signup_prompt(app=app)
  File "/mnt/c/Users/kdwkd/PycharmProjects/book-manager/src/prompt/start.py", line 77, in signup_prompt
    user_id = input_with_validation(
  File "/mnt/c/Users/kdwkd/PycharmProjects/book-manager/src/core/valid.py", line 19, in input_with_validation
    log.debug(f"{prompt}:: {value}")
Message: 'ID를 입력하세요: :: \udce3\udc85asfasf'
Arguments: ()
ID가 4자리 이상이어야 합니다!!  다른 ID를 입력하세요.
ID를 입력하세요:
