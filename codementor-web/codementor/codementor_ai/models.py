from django.db import models
import json

# Create your models here.

class CodeMentorBase(models.Model):
  code_input = models.JSONField(default=dict, blank=False)

  def __str__(self):
    words = json.loads(self.code_input)['code_input'].split()[5]
    return f"Code Review: {words}"

class CodeReview(CodeMentorBase):
    code_review = models.JSONField(default=dict, blank=True)

class TestCase(CodeMentorBase):
    test_case = models.JSONField(default=dict, blank=True)

class CodeDebug(CodeMentorBase):
    code_debug = models.JSONField(default=dict, blank=True)
