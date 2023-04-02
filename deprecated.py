# def get_oscar(id):
#     headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
#     full_info = requests.get(f"https://www.kinopoisk.ru/film/{id}/awards/", headers=headers)
#     while not('Награды' in full_info.text):
#         headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#         }
#         full_info = requests.get(f"https://www.kinopoisk.ru/film/{id}/awards/", headers=headers)
#         print(str(id) + 'что-то не так оскар')
#         time.sleep(random.randint(5, 10))

#     with open("log-oscar.txt", 'a') as f:
#         f.write(full_info.text)
#         f.write("\n\n*************************\n\n")

#     return 'Оскар, ' in full_info.text


# def get_about(id):
#     driver_path = '/home/evgeny/freelance/parser_tiktok/chromedriver_linux64/chromedriver'
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument("--disable-blink-features=AutomationControlled")

#     driver = webdriver.Chrome(executable_path=driver_path, options=options)

#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         'source': '''
#             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
#             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
#             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;

#         '''
#     })

#     url = f'https://www.kinopoisk.ru/film/{id}/'
#     driver.get(url)
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')

#     soup.prettify()
#     with open("log-about.txt", 'a') as f:
#         f.write(soup.text)
#         f.write("\n\n*************************\n\n")

#     while not('Награды' in soup.text):
#         driver.get(url)
#         html = driver.page_source
#         soup = BeautifulSoup(html, 'html.parser')
#         print(str(id) + '@о фильме@')
#         time.sleep(random.randint(5, 10))

#     driver.quit()
#     if soup.find('p', {'class': 'styles_paragraph__wEGPz'}):
#         return soup.find('p', {'class': 'styles_paragraph__wEGPz'}).text
#     return "нет описания"