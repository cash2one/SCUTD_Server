# coding: utf-8

from leancloud import Engine

from app import app
from tools import read_sojump
from leancloud_path import write_leancloud


engine = Engine(app)


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'
@engine.define
def upload_sojump(**params):

	read_sojump().get_jump_list(1)
	read_sojump().get_jump_list(2)

	return True

@engine.define
def chenge_school_type(**params):

	write_leancloud().change_school_type()
	

	return True

@engine.define
def update_school_type(**params):

	write_leancloud().update_school_type()
	

	return True


@engine.define
def public_magazine(**params):
	write_leancloud().public_magazine(0)
	write_leancloud().public_magazine(1)
	return True



