
from .models import Tag


def _get_tags(tag_string):
    """ Take the string of tags, and convert into tags object
        If tags already exist, dont create.
        Return a list of tag objects to add to the project
    """
    print "inside get_tags, string is: ", tag_string
    tag_objects_list = []
    # remove all whitespaces
    tag_string_cleaned = tag_string.replace(" ", "")
    tokens = tag_string_cleaned.split(',')
    for tok in tokens:
        try:
            tag_object = Tag.objects.get(tag_name=tok)
        except Tag.DoesNotExist:
            tag_object = Tag(tag_name=tok)
            tag_object.save()
        if tag_object not in tag_objects_list:
            tag_objects_list.append(tag_object)
    return tag_objects_list
