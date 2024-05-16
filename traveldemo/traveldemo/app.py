import panel as pn
import pandas as pd 
from loguru import logger
import os 
import traceback
import re 

try:
    import py_iris_utils.connection as connection
    from py_iris_utils.connection import load_config
    from paneltools.golden import IRISGoldenTemplate

except:
    traceback.print_exc()

from config import template_css, app_config, stopwords
from sentence_transformers import SentenceTransformer

from sqlalchemy import text 

from dotenv import load_dotenv
load_dotenv()

result_count = 25
ifind_search = """Select top {count} name, general, todo, 
%iFind.Rank('%iFind.Rank.TFIDF', 'User.Place', 'todoifind', %ID, '{query}') As Rank
from Place
WHERE %ID %FIND search_index(todoifind, '{query}')
Order by Rank Desc"""

# Use ENVVAR or from config dir in project root
CONFIG_PATH = os.environ.get("IRIS_VECTOR_DEMO_CONFIG", "../config/demo_config.json")
config = load_config(CONFIG_PATH) 

logger.info(f"Starting app.py with Config path = {CONFIG_PATH} and config = {config}")

def find_all_snippets(text: str, words: list, char_window: int, max_snippets: int = 5):
    # Return a list of tuples with starting and ending index where any word in the words list matches in the text
    matches = [(match.start(), match.end()) for match in re.finditer(r'\b(?:' + '|'.join(words) + r')\b', text.lower())]

    total_matches = f'Matches = {len(matches)}'

    text_snippets = f'<span style="white-space: pre-wrap; font:Helvetica, Arial, sans-serif;">'
    counter = 0
    for item in matches:
        text_snippets += f"...{text[item[0]-char_window: item[0]]}<b>{text[item[0]:item[1]]}</b>{text[item[1]: item[1]+char_window]}...\n"
        counter += 1
        if counter == max_snippets:
            break
       # text_snippets += "..." + text[item[0]-char_window:item[1]+char_window] + "...\n"
    text_snippets += "</span>"
    return text_snippets 

def regular_search(window_char: int=55, max_snippets: int = 3):
    search_list = [w for w in search_text.value.split()if w.lower() not in stopwords]
    cleaned_search = " OR ".join([w for w in search_list])
    keywords.value = cleaned_search
    query =  ifind_search.format(count=result_count, query=cleaned_search)
    print(query)
    testdata = pd.read_sql(query, iris.engine.connect())

    window_chars = 55
    max_snippets = 3
    
    testdata['sample matches'] = testdata['todo'].apply(lambda x: find_all_snippets(x, search_list, window_chars, max_snippets))
    
    return testdata

def vector_search():
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    embeddings = model.encode(search_text.value, normalize_embeddings=True).tolist()
    
    sql1 = f"""
                SELECT TOP {result_count} name, general, todo FROM Place 
                ORDER BY VECTOR_DOT_PRODUCT(todo_vector, TO_VECTOR(:search_vector)) DESC
            """
    sql2 = """
                SELECT distinct(place), sum(VECTOR_DOT_PRODUCT(fullactivity_vector, TO_VECTOR(:search_vector))) as VectorSum
                from Activity
                group by place
                order by VectorSum desc
                
        """

    with iris.engine.connect() as conn:
        with conn.begin():
            sql = text(sql1)
            print(sql)
            results = pd.read_sql(sql, iris.engine.connect(), params={'search_vector': str(embeddings)})
            #results = pd.read_sql(sql, iris.engine.connect(), params={'search_vector': str(embeddings)})
            #results = conn.execute(sql, params={'search_vector': str(embeddings)}).fetchall()
    return results

 
def search_button_handler(event):

    if vector_checkbox.value:
        table_view.hidden_columns= ['Rank', 'general']
        results_df = vector_search()
        if 'todo' in results_df:
            results_df['todo'] = results_df['todo'].str.slice(0,1500) + "..."
        table_view.value = results_df
    else:
        table_view.value = regular_search()

def vector_checkbox_handler(event):
    pass


# pn.extension('tabulator')

png_pane = pn.pane.PNG('/assets/images/TravelSearchPageWide2.png',  height=200)
header_row  = pn.Row(png_pane)
header_image_card = pn.Card(png_pane, hide_header=True)

template = IRISGoldenTemplate(
        title=app_config.get("name"),
        header=[],
        header_background = '#FFFFFF',
        sidebar_width=10)

pn.extension('tabulator')

iris = connection.IRISConnection(config)

def match_formatter(cell, formatterParams, onRendered) -> str:
    return f"<pre>{cell.getValue()}</pre>"

tabulator_formatters = { 'general': {'type': 'textarea'}, 'todo': {'type': 'textarea'}, 'sample matches': {'type': 'html'},
                        'index': {'title': 'Rank', 'type' : 'int'}} 

# cell.getElement().style.whiteSpace = "pre-wrap";
#Tabulator.extendModule("format", "formatters", {
#     file:function(cell, formatterParams){
#         return "<img class='fileicon' src='/images/fileicons/" + cell.getValue() + ".png'></img>";
#     },
# });

# Get empty dataset to init grid
testdata = pd.read_sql("Select top 1 '' as rank, name, '' as sample_matches  from Place P where name = '12341234'", iris.engine.connect())

def row_selection(df: pd.DataFrame):
    print(f"Selected {df}")

def cell_click(event):
    print(f"Clicked {event}")

table_view = pn.widgets.Tabulator(testdata, pagination='remote', page_size=10, 
                                  layout='fit_columns', sizing_mode="stretch_width",
                                  formatters=tabulator_formatters, hidden_columns= ['Rank', 'general', 'todo'], theme='simple', 
                                  disabled=True, selectable_rows=row_selection, selectable=True)

table_view.on_click(cell_click) 

keywords = pn.widgets.StaticText(name='', value='', align='end')


search_text = pn.widgets.TextAreaInput(name="", value="I would like to snorkel and visit historic sites", height=70, width=500)
search_button = pn.widgets.Button(name="Search", align='end', button_type='primary', button_style='outline', )
vector_checkbox = pn.widgets.Checkbox(name='Vector' , align='end')
search_row = pn.Row(search_text, search_button, vector_checkbox, keywords)

pn.bind(search_button_handler, search_button, watch=True)

travel_results_card = pn.Card(table_view, name='travel')

main_col = pn.Column(header_image_card, search_row, table_view )
template.main.append(main_col)
template.main.title = "Travel Demo"


# template.main.append(pn.Card(textarea, name='text'))
# template.main.append(header_image_card)
# template.main.append(pn.Card(table_view, name='travel'))

pn.extension(raw_css=[template_css])

template.servable() 

logger.info(f"Finished loading {__name__}")