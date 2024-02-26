from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

import re

def is_valid_channel_url(url):
    # Regular expression patterns for YouTube channel URLs
    channel_patterns = [
        r'^https?://(www\.)?youtube\.com/channel/[A-Za-z0-9_-]+$',
        r'^https?://(www\.)?youtube\.com/c/[A-Za-z0-9_-]+$',
        r'^https?://(www\.)?youtube\.com/user/[A-Za-z0-9_-]+$',
        r'^https?://(www\.)?youtube\.com/(c/|user/|@)([a-zA-Z0-9_-]+)',
        r'^https?://youtube\.com/@[A-Za-z0-9_-]+(\?.*)?$'
    ]
    return any(re.match(pattern, url) for pattern in channel_patterns)

def is_valid_playlist_url(url):
    # Regular expression for YouTube playlist URLs
    youtube_playlist_patterns = [
        r'^https?://(www\.)?youtube\.com/playlist\?list=[a-zA-Z0-9_-]+(&.*)?$',
        r'^https?://youtube\.com/playlist\?list=[a-zA-Z0-9_-]+(&.*)?$',
        r'^https?://(www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+&list=[a-zA-Z0-9_-]+(&.*)?$',
        r'^https?://youtu\.be/[a-zA-Z0-9_-]+\?list=[a-zA-Z0-9_-]+(&.*)?$'
    ]
    return any(re.match(pattern, url) for pattern in youtube_playlist_patterns)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class CustomPasswordResetForm(PasswordResetForm):

    def save(self, domain_override=None, use_https=False, token_generator=default_token_generator, from_email=None, request=None, extra_email_context=None, **kwargs):
        email = self.cleaned_data["email"]
        
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
                
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {})
            }

            self.send_mail(
                'registration/custom_password_reset_subject.txt',
                'registration/custom_password_reset_email.html',
                context,
                from_email,
                email,
                html_email_template_name='registration/custom_password_reset_email.html'
            )

class CompetitiveAnalysisTypeForm(forms.Form):
    ANALYSIS_CHOICES = (
        ('channel', 'Compare between channels'),
        ('playlist', 'Compare between playlists'),
    )
    analysis_type = forms.ChoiceField(choices=ANALYSIS_CHOICES)
    

class myChannelPlaylistInputForm(forms.Form):
    input_text = forms.CharField(label='', max_length=255)  # Initially leave label empty

    def __init__(self, *args, **kwargs):
        # Extract the analysis_type argument if provided
        self.analysis_type = kwargs.pop('analysis_type', None)
        super(myChannelPlaylistInputForm, self).__init__(*args, **kwargs)

    def clean_input_text(self):
        print('cleaining input text')
        print(self.analysis_type)
        input_text = self.cleaned_data['input_text']
        if self.analysis_type == 'channel':
            # Validate as channel URL
            if not is_valid_channel_url(input_text):
                raise ValidationError("Please enter a valid YouTube channel URL.")
        elif self.analysis_type == 'playlist':
            # Validate as playlist URL
            if not is_valid_playlist_url(input_text):
                raise ValidationError("Please enter a valid YouTube playlist URL.")
        return input_text

COUNTRY_CHOICES = [
    ('', '---------'),
    ('AF', 'Afghanistan'),
    ('AX', 'Åland Islands'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia (Plurinational State of)'),
    ('BQ', 'Bonaire, Sint Eustatius and Saba'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CV', 'Cabo Verde'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos (Keeling) Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo (Democratic Republic of the)'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Côte d\'Ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CW', 'Curaçao'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czechia'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('SZ', 'Eswatini'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French Southern Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GG', 'Guernsey'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HM', 'Heard Island and McDonald Islands'),
    ('VA', 'Holy See'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran (Islamic Republic of)'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IM', 'Isle of Man'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JE', 'Jersey'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea (Democratic People\'s Republic of)'),
    ('KR', 'Korea (Republic of)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Lao People\'s Democratic Republic'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macao'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia (Federated States of)'),
    ('MD', 'Moldova (Republic of)'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PS', 'Palestine, State of'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('MK', 'Republic of North Macedonia'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('RE', 'Réunion'),
    ('BL', 'Saint Barthélemy'),
    ('SH', 'Saint Helena, Ascension and Tristan da Cunha'),
    ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'),
    ('MF', 'Saint Martin (French part)'),
    ('PM', 'Saint Pierre and Miquelon'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome and Principe'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('RS', 'Serbia'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SX', 'Sint Maarten (Dutch part)'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('GS', 'South Georgia and the South Sandwich Islands'),
    ('SS', 'South Sudan'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SJ', 'Svalbard and Jan Mayen'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan, Province of China'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania, United Republic of'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TC', 'Turks and Caicos Islands'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('GB', 'United Kingdom of Great Britain and Northern Ireland'),
    ('US', 'United States of America'),
    ('UM', 'United States Minor Outlying Islands'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela (Bolivarian Republic of)'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands (British)'),
    ('VI', 'Virgin Islands (U.S.)'),
    ('WF', 'Wallis and Futuna'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe'),
]


LANGUAGE_CHOICES = [
    ('', '---------'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ru', 'Russian'),
    ('zh', 'Chinese'),
    ('ja', 'Japanese'),
    ('ar', 'Arabic'),
    ('hi', 'Hindi'),
    ('bn', 'Bengali'),
    ('pa', 'Punjabi'),
    ('id', 'Indonesian'),
    ('ko', 'Korean'),
    ('tr', 'Turkish'),
    ('vi', 'Vietnamese'),
    ('pl', 'Polish'),
    ('nl', 'Dutch'),
    ('ro', 'Romanian'),
    ('hu', 'Hungarian'),
    ('sv', 'Swedish'),
    ('fi', 'Finnish'),
    ('da', 'Danish'),
    ('no', 'Norwegian'),
    ('cs', 'Czech'),
    ('el', 'Greek'),
    ('he', 'Hebrew'),
    ('th', 'Thai')
    ]

ORDER_CHOICES = [
    ('relevance', 'Relevance'),
    ('date', 'Date'),
    ('rating', 'Rating'),
    ('title', 'Title'),
    ('videoCount', 'Video Count'),
    ('viewCount', 'View Count'),
]


VIDEO_CATEGORIES = [
    ('1', 'Film & Animation'),
    ('2', 'Autos & Vehicles'),
    ('10', 'Music'),
    ('15', 'Pets & Animals'),
    ('17', 'Sports'),
    ('18', 'Short Movies'),
    ('19', 'Travel & Events'),
    ('20', 'Gaming'),
    ('21', 'Videoblogging'),
    ('22', 'People & Blogs'),
    ('23', 'Comedy'),
    ('24', 'Entertainment'),
    ('25', 'News & Politics'),
    ('26', 'Howto & Style'),
    ('27', 'Education'),
    ('28', 'Science & Technology'),
    ('29', 'Nonprofits & Activism'),
    ('30', 'Movies'),
    ('31', 'Anime/Animation'),
    ('32', 'Action/Adventure'),
    ('33', 'Classics'),
    ('34', 'Comedy'),
    ('35', 'Documentary'),
    ('36', 'Drama'),
    ('37', 'Family'),
    ('38', 'Foreign'),
    ('39', 'Horror'),
    ('40', 'Sci-Fi/Fantasy'),
    ('41', 'Thriller'),
    ('42', 'Shorts'),
    ('43', 'Shows'),
    ('44', 'Trailers'),
]

class YouTubeSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Extract the analysis_type argument if provided
        self.analysis_type = kwargs.pop('analysis_type', None)
        super(YouTubeSearchForm, self).__init__(*args, **kwargs)

        
    search_query = forms.CharField(label='Search Query', max_length=100, required=True)
    order = forms.ChoiceField(label='Order', choices=ORDER_CHOICES, required=False, initial='relevance')
    region_code = forms.ChoiceField(label='Region Code', choices=COUNTRY_CHOICES, required=False)
    language = forms.ChoiceField(label='Language', choices=LANGUAGE_CHOICES, required=False)


class YouTubeCategorySearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Extract the analysis_type argument if provided
        self.analysis_type = kwargs.pop('analysis_type', None)
        super(YouTubeCategorySearchForm, self).__init__(*args, **kwargs)

    category = forms.ChoiceField(label='Category', choices=VIDEO_CATEGORIES, required=True)
    order = forms.ChoiceField(label='Order', choices=ORDER_CHOICES, required=False, initial='relevance')
    region_code = forms.ChoiceField(label='Region Code', choices=COUNTRY_CHOICES, required=False)
    language = forms.ChoiceField(label='Language', choices=LANGUAGE_CHOICES, required=False)

class ChannelsListInput(forms.Form):
    
    def __init__(self, *args, **kwargs):
        # Extract the analysis_type argument if provided
        self.analysis_type = kwargs.pop('analysis_type', None)
        super(ChannelsListInput, self).__init__(*args, **kwargs)

    
    channel_url_1 = forms.URLField(label='Channel URL 1', required=True)
    channel_url_2 = forms.URLField(label='Channel URL 2', required=False)
    channel_url_3 = forms.URLField(label='Channel URL 3', required=False)
    channel_url_4 = forms.URLField(label='Channel URL 4', required=False)

    
    def clean_channel_url_1(self):
        return self.clean_url('channel_url_1', 1)

    def clean_channel_url_2(self):
        return self.clean_url('channel_url_2', 2)

    def clean_channel_url_3(self):
        return self.clean_url('channel_url_3', 3)

    def clean_channel_url_4(self):
        return self.clean_url('channel_url_4', 4)


    def clean_url(self, field_name, field_number):
        url = self.cleaned_data.get(field_name)
        if url and self.analysis_type == 'channel' and not is_valid_channel_url(url):
            raise ValidationError(f"Please enter a valid YouTube channel URL for Channel {field_number}.")
        elif url and self.analysis_type == 'playlist' and not is_valid_playlist_url(url):
            raise ValidationError(f"Please enter a valid YouTube playlist URL for Playlist {field_number}.")
        return url

CHOICES = [
    ('input_list', 'Input a list of channels'),
    ('search', 'Search channels'),
    # ('category', 'Select a category'),
]

class FindInitialChoiceForm(forms.Form):
    
    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Select an option")
    
    def __init__(self, *args, **kwargs):
        # Extract the analysis_type argument if provided
        self.analysis_type = kwargs.pop('analysis_type', None)
        super(FindInitialChoiceForm, self).__init__(*args, **kwargs)


OUTPUT_CHOICES = [
    ('dataset', 'A CSV data set'),
    ('report', 'A PDF report'),
]

class OutputChoiceForm(forms.Form):
    choice_output = forms.MultipleChoiceField(
        choices=OUTPUT_CHOICES,
        widget=forms.CheckboxSelectMultiple,  # Correct widget for multiple choices
        label="Select an option"
    )

from django import forms
from django.core.exceptions import ValidationError
import re

class VideoAnalysisInputForm(forms.Form):
    video_url = forms.CharField(label='', max_length=255)  # Initially leave label empty
    
    def clean_video_url(self):
        video_url = self.cleaned_data['video_url']
        youtube_video_pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[a-zA-Z0-9_-]{11}(&.*)?$'


        if not re.match(youtube_video_pattern, video_url):
            raise ValidationError("Please enter a valid YouTube video URL.")
        return video_url
    
class PlaylistAnalysisInputForm(forms.Form):
    playlist_url = forms.URLField(label='Playlist URL', required=True)

    def clean_playlist_url(self):
        playlist_url = self.cleaned_data['playlist_url']
        youtube_playlist_pattern = r'^(https?://)?(www.youtube.com|youtube.com)/playlist\?list=[a-zA-Z0-9_-]+(&.*)?$'
        
        if not re.match(youtube_playlist_pattern, playlist_url):
            raise ValidationError("Please enter a valid YouTube playlist URL.")
        return playlist_url
    
class ChannelAnalysisInputForm(forms.Form):
    channel_url = forms.URLField(label='Channel URL', required=True)

    def clean_channel_url(self):
        channel_url = self.cleaned_data['channel_url']
        if(not is_valid_channel_url(channel_url)):       
            raise ValidationError("Please enter a valid YouTube channel URL.")
        return channel_url
    

class VideoRetrivingInputForm(forms.Form):
    search_query = forms.CharField(label='Search Query', max_length=100, required=True)
    num_of_videos = forms.IntegerField(label='Number Of Videos:', required=True)
    order = forms.ChoiceField(label='Order', choices=ORDER_CHOICES, required=False, initial='relevance')
    region_code = forms.ChoiceField(label='Region Code', choices=COUNTRY_CHOICES, required=False)
    language = forms.ChoiceField(label='Language', choices=LANGUAGE_CHOICES, required=False)

    def clean_search_query(self):
        video_url = self.cleaned_data['search_query']
        youtube_video_pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[a-zA-Z0-9_-]{11}(&.*)?$'

        
        if not re.match(youtube_video_pattern, video_url):
            raise ValidationError("Please enter a valid YouTube video URL.")
        return video_url
    
    
class PostAnalysisInputForm(forms.Form):
    post_url = forms.URLField(label='Post URL', required=True)

    def clean_post_url(self):
        post_url = self.cleaned_data['post_url']
        instagram_post_pattern = r'https?://www.instagram.com/p/([a-zA-Z0-9_-]+)/?'

        match = re.match(instagram_post_pattern, post_url)
        if not match:
            raise ValidationError("Please enter a valid Instagram post URL.")
        
        return post_url 
   
class ProfileAnalysisInputForm(forms.Form):
    profile_url = forms.URLField(label='Profile URL', required=True)

    def clean_profile_url(self):
        profile_url = self.cleaned_data['profile_url']
        instagram_profile_pattern = r'^(https?:\/\/)?(www\.)?instagram\.com\/[a-zA-Z0-9_.]+\/?$'

        match = re.match(instagram_profile_pattern, profile_url)
        if not match:
            raise ValidationError("Please enter a valid Instagram profile URL.")

        return profile_url
    
class TopicTrendAnalysisInputForm(forms.Form):
    hashtag = forms.CharField(label='Hashtag', required=True)

    def clean_profile_url(self):
        hashtag = self.cleaned_data['hashtag']
        return hashtag