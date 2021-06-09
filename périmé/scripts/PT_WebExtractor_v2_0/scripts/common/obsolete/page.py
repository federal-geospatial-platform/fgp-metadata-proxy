import os
import sys
import urllib2
from bs4 import NavigableString, BeautifulSoup
import collections
import math
import datetime
import json
import csv
from csv import reader
import requests
import urlparse
import argparse
import codecs
import cStringIO
import re
import pprint
import traceback

class Page:
    def __init__(self, id, title, method=None):
        self.id = id
        self.title = title
        self.method = method
        self.urls = collections.OrderedDict()
        self.method_args = collections.OrderedDict()
        self.questions = collections.OrderedDict()
        self.opts = None
        self.defaults = collections.OrderedDict()

    def set_title(self, title):
        ''' Sets the title of the page
        :param title: The title string for the page.
        :return: None
        '''
        self.title = title

    def get_title(self):
        ''' Gets the title of the page.
        :return: The title of the page.
        '''
        return self.title

    def get_arcgis_urls(self, other_word=None):
        ''' Gets all the ArcGIS Online URLs
        :return: A list of ArcGIS URLs.
        '''
        url_list = []
        for key, value in self.urls.items():
            if key.find('url') > -1:
                if isinstance(value, list):
                    for url in value:
                        if other_word is None:
                            if url.find('arcgis') > -1:
                                url_list.append(url)
                        else:
                            if url.find('arcgis') > -1 or url.find(other_word) > -1:
                                url_list.append(url)
                else:
                    if other_word is None:
                        if value.find('arcgis') > -1:
                            url_list.append(value)
                    else:
                        if value.find('arcgis') > -1 or value.find(other_word) > -1:
                            url_list.append(value)

        return url_list


    def get_arg(self, arg_name):
        ''' Gets a specific argument from the method_args dictionary.
        :param arg_name: The argument name.
        :return: The argument value
        '''
        return self.method_args[arg_name]

    def set_arg(self, arg_name, arg_val):
        ''' Sets a specific argument from the method_args dictionary.
        :param arg_name: The argument name.
        :param arg_val: The argument value to set.
        :return: The argument value
        '''
        self.method_args[arg_name] = arg_val

    def get_args_list(self):
        ''' Gets a list of method arguments.
        :return: The list of method arguments.
        '''
        return self.method_args.keys()

    def get_args(self):
        ''' Gets a dictionary of method arguments.
        :return: A dictionary of method arguments.
        '''
        return self.method_args

    def set_args(self, arg_list):
        ''' Sets the keys in the method argument dictionary with emtpy values.
        :param arg_list: A list of arguments to add to the dictionary
        :return: None
        '''
        arg_list.remove('self')
        for m_arg in arg_list:
            # Set the value of the argument
            if m_arg in self.defaults.keys():
                self.method_args[m_arg] = self.defaults[m_arg]
            else:
                self.method_args[m_arg] = None

            if m_arg == 'word':
                self.questions[m_arg] = "Please enter a search word"
            elif m_arg == 'downloadable':
                self.questions[m_arg] = "Would you like to filter for downloadable content in the '%s' page?" \
                                        % self.title
			elif m_arg == 'ds_type':
				self.questions[m_arg] = "Please enter the dataset type for the '%s' page" % self.title
            else:
                # Get default value
                def_val = ''
                if m_arg in self.defaults.keys():
                    def_val = self.defaults[m_arg]

                # Get the available options
                avail_opts = ''
                if self.opts is not None and m_arg in self.opts.keys():
                    opts = self.opts[m_arg]
                    # If the default is not in the list of options, add it
                    if not def_val == '' and def_val not in opts:
                        opts.append(def_val)
                    if len(opts) > 0:
                        avail_opts = ', '.join(['"%s"' % o for o in opts])

                # Create the question text
                root_question = "Please enter the %s for the '%s' page" % (m_arg, self.title)

                if def_val == '':
                    if avail_opts == '':
                        opts_text = "(press enter to run all)"
                    else:
                        opts_text = "(available options: %s or press enter to run all)" % avail_opts
                else:
                    if avail_opts == '':
                        opts_text = "[%s]" % def_val
                    else:
                        opts_text = "(available options: %s) [%s]" % (avail_opts, def_val)

                self.questions[m_arg] = "%s %s" % (root_question, opts_text)

    def add_default(self, arg_name, arg_val):
        ''' Adds a default value for a specified argument.
        :param arg_name: The argument name
        :param arg_val: The argument default value
        :return: None
        '''

        self.defaults[arg_name] = arg_val

    def add_url(self, title, url):
        ''' Adds a web page to the list of URLs.
        :param title: The variable title of the web page.
        :param url: The URL of the web page.
        :return: None
        '''
        self.urls[title] = url

    def get_id(self):
        ''' Gets the ID of the current page.
        :return: The ID of the current page.
        '''
        return self.id

    def get_questions(self):
        ''' Gets the dictionary of questions for the page.
        :return: A dictionary of the page's questions.
        '''
        return self.questions

    def get_opts(self):
        ''' Gets the options for the method arguments
        :return: A dictionary of the method arguments and available values
        '''

        return self.opts

    def set_opts(self, opts):
        ''' Sets the available options for a method argument.
        :param opts: A dictionary like
                    {arg_name: [arg_val, arg_val, arg_val, ...],
                     arg_name: [arg_val, arg_val, arg_val, ...],
                     ...
                    }
        :return: None
        '''

        self.opts = opts

    def get_url(self, param):
        ''' Gets a URL from the list of URLs.
        :param param: The URL name.
        :return: The URL containing param.
        '''
        if param in self.urls:
            return self.urls[param]
        else:
            print "\nPage WARNING: The given URL type is not available."

    def get_url_list(self):
        ''' Gets the URL list.
        :return: The URL list.
        '''

        url_list = []
        for key, value in self.urls.items():
            if key.find('url') > -1:
                if isinstance(value, list):
                    for url in value:
                        url_list.append(url)
                else:
                    url_list.append(value)

        return url_list

    def get_urls(self):
        ''' Gets a list of the URLs of the page.
        :return: A list of URLs.
        '''
        return self.urls