# Amara, universalsubtitles.org
#
# Copyright (C) 2015 Participatory Culture Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see
# http://www.gnu.org/licenses/agpl-3.0.html.

"""utils.forms.languages -- form fields for selecting languages."""

from django import forms

from utils.translation import get_language_choices

class MultipleLanguageChoiceField(forms.MultipleChoiceField):
    # TODO: implement a nicer widget for selecting multiple languages
    widget = forms.SelectMultiple

    def __init__(self, choices=None, *args, **kwargs):
        if choices is None:
            choices = self.calc_language_choices()
        super(MultipleLanguageChoiceField, self).__init__(
            *args, choices=choices, **kwargs)

    def calc_language_choices(self):
        return get_language_choices()

