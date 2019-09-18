from elasticsearch_dsl import analyzer


lowercase = analyzer(
    'lowercase_analyzer',
    filter=['standard', 'lowercase']
)

url = analyzer(
    'url_analyzer',
    tokenizer='uax_url_email'
)
