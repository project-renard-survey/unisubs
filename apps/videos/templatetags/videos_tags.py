# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
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
from django import template

register = template.Library()

@register.inclusion_tag('videos/_feature_video.html', takes_context=True)
def feature_video(context, video):
    context['video'] = video
    return context

@register.filter
def is_follower(obj, user):
    #obj is Video or SubtitleLanguage
    if not user.is_authenticated():
        return False
    
    if not obj:
        return False
    
    return obj.followers.filter(pk=user.pk).exists()