from TemplatesData import GestureTemplates
from Steps import Steps

#Process the Template points
class Unistroke:

    #Template Samples
    def GetTemplates(self):

        GT = GestureTemplates()
        steps = Steps()
        #Collection of Processed Templates
        templates = [steps.GetTemplate("triangle", GT.triangle),
                     steps.GetTemplate("x", GT.cross),
                     steps.GetTemplate("rectangle", GT.rectangle),
                     steps.GetTemplate("circle", GT.circle),
                     steps.GetTemplate("check", GT.check),
                     steps.GetTemplate("caret", GT.caret),
                     steps.GetTemplate("zigzag", GT.zigzag),
                     steps.GetTemplate("arrow", GT.arrow),
                     steps.GetTemplate("left_square_brace", GT.lsb),
                     steps.GetTemplate("right_square_brace", GT.rsb),
                     steps.GetTemplate("v", GT.vstroke),
                     steps.GetTemplate("delete", GT.delete),
                     steps.GetTemplate("left_curly_brace", GT.lcb),
                     steps.GetTemplate("right_curly_brace", GT.rcb),
                     steps.GetTemplate("star", GT.star),
                     steps.GetTemplate("pigtail", GT.pigtail)]

        return templates

    def GetTemplatesProtractor(self):

        GT = GestureTemplates()
        steps = Steps()
        #Collection of Processed Templates
        templates = [steps.GetTemplate("triangle", GT.triangle, True),
                     steps.GetTemplate("x", GT.cross, True),
                     steps.GetTemplate("rectangle", GT.rectangle, True),
                     steps.GetTemplate("circle", GT.circle, True),
                     steps.GetTemplate("check", GT.check, True),
                     steps.GetTemplate("caret", GT.caret, True),
                     steps.GetTemplate("zigzag", GT.zigzag, True),
                     steps.GetTemplate("arrow", GT.arrow, True),
                     steps.GetTemplate("left_square_brace", GT.lsb, True),
                     steps.GetTemplate("right_square_brace", GT.rsb, True),
                     steps.GetTemplate("v", GT.vstroke, True),
                     steps.GetTemplate("delete", GT.delete, True),
                     steps.GetTemplate("left_curly_brace", GT.lcb, True),
                     steps.GetTemplate("right_curly_brace", GT.rcb, True),
                     steps.GetTemplate("star", GT.star, True),
                     steps.GetTemplate("pigtail", GT.pigtail, True)]

        return templates
