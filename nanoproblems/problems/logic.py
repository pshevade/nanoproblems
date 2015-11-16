
from .models import Tag
import comments.logic as comment_service


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


def addcommentproblem(request, problem):
    """ Add a comment to a given problem.
    """
    comment = comment_service.createcomment(request)
    if comment:
        problem.comments.add(comment)
        return True
    else:
        print "something went wrong, couldn't create a new comment for problem."
        return False


def editcommentproblem(request, problem, comment_id):
    """ Edit comment.
    """
    comment = comment_service.checkcommentexists(request, comment_id)
    # Return false if comment is not in this problem! 
    if comment:
        if comment not in problem.comments:
            return False
        comment_service.editcomment(request, comment)
        return True
    else:
        print "something went wrong, couldn't find comment"
        return False


def deletecommentproblem(request, problem, comment_id):
    comment = comment_service.checkcommentexists(request, comment_id)
    if comment:
        if comment in problem.comments:
            problem.comments.remove(comment)
        else:
            return False
        comment_service.deletecomment(request, comment)
        return True
    else:
        print "something went wrong, couldn't find comment"
        return False
