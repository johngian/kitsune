from celery import task

from kitsune.search.v2 import documents


DOCUMENT_CLASSES = {
    'ProfileDocument': documents.ProfileDocument
}


@task
def index_object(document_type, obj_id):
    """Index object in ES"""
    doc_cls = DOCUMENT_CLASSES[document_type]
    doc = doc_cls.get_extracted_document(obj_id)
    doc.meta.id = obj_id
    doc.save()


@task
def unindex_object(document_type, obj_id):
    """Unindex object from ES"""
    doc_cls = DOCUMENT_CLASSES[document_type]
    doc = doc_cls.get(id=obj_id)
    doc.delete()
