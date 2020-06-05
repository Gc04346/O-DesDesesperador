from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from django_project.apps.contrib.models.base_model import BaseModel
from django_project.settings.base import DEFAULT_PRICES

# lista de instrumentos
INSTRUMENTS = (
    ('v', _('Guitar')),
    ('g', _('Eletric Guitar')),
    ('b', _('Bass')),
    ('t', _('Keyboard')),
    ('bt', _('Drums')),
    ('bvt', _('Backing Vocal (Tenor)')),
    ('bvs', _('Backing Vocal (Soprano)')),
    ('bvc', _('Backing Vocal (Contralto)'))
)

# lista de tipos de eventos
EVENT_TYPES = (
    ('Show', 'Show'),
    ('Marcha pra Jesus', 'Marcha pra Jesus'),
    ('Festival', 'Festival'),
    ('Congresso', 'Congresso'),
    ('Culto', 'Culto')
)

# lista de status do evento
EVENT_STATUSES = (
    ('PE', _('Pending')),
    ('YES', _('Confirmed')),
    ('NO', _('Refused')),
)

# lista de opcoes que indicam se o evento correu bem
EVENT_ALRIGHT_CHOICES = (
    ('OK', _('Everything went well')),
    ('NO', _('I had problems')),
    ('NA', _(' ')),
)

# lista de metodos de pagamento
PAYMENT_METHODS = (
    ('DD', 'Direct Deposit'),
    ('BT', 'Bank Ticket'),
    ('CC', 'Credit Card'),
)


def get_instrument_name_by_type(instrument_type):
    """
        retorna o valor do instumento, e nao seu codigo
        Args:
            instrument_type: str
    """
    for instrument in INSTRUMENTS:
        if instrument_type == instrument[0]:
            return instrument[1]

    return _('N/A')


def get_tutorial_video_by_user(user):
    """
        Retorna o video para ser usado como tutorial para o usuario
        Args:
            user: User
    """
    user_type = get_user_type(user)
    if user_type == 'artist':
        return "https://www.youtube.com/embed/C5wF4_wopt8"
    if user_type == 'producer':
        return "https://www.youtube.com/embed/yZ8crWJLxHI"
    if user_type == 'musician':
        return "https://www.youtube.com/embed/yIup9TmU-9s"
    if user_type == 'music_director':
        return "https://www.youtube.com/embed/vIJbqwWgoDc"
    else:
        return ""


def has_accepted_use_terms(user_id):
    """
        verifica se o usuario aceitou os termos de uso
        Args:
            user_id: int
    """
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return False
    user_type = get_user_type(user)
    if user_type == 'artist':
        return Artist.objects.get(user=user).accepted_use_terms
    if user_type == 'producer':
        return Producer.objects.get(user=user).accepted_use_terms
    if user_type == 'musician':
        return Musician.objects.get(user=user).accepted_use_terms
    if user_type == 'music_director':
        return MusicDirector.objects.get(user=user).accepted_use_terms
    if user_type == 'admin':
        return True


def get_user_type(user):
    """
        retorna o modelo de usuario do user em questao
        Args:
            user: User
    """
    if user.is_staff:
        return 'admin'
    elif hasattr(user, 'artist'):
        return 'artist'
    elif hasattr(user, 'producer'):
        return 'producer'
    elif hasattr(user, 'musician'):
        return 'musician'
    elif hasattr(user, 'musicdirector'):
        return 'music_director'
    else:
        return None


def get_user_attribute(user, attribute):
    """
        implementacao generica do metodo 'built-in' getattr, com base no modelo do usuario
        Args:
            user: User
            attribute: string
    """
    if hasattr(user, 'artist'):
        return getattr(user.artist, attribute, None)
    elif hasattr(user, 'producer'):
        return getattr(user.producer, attribute, None)
    elif hasattr(user, 'musician'):
        return getattr(user.musician, attribute, None)

    elif hasattr(user, 'musicdirector'):
        return getattr(user.musicdirector, attribute, None)
    else:
        return None


def set_user_attribute(user, attribute, value):
    """
        implementacao generica do metodo 'built-in' setattr, com base no modelo do usuario
        Args:
            user: User
            attribute: string
    """
    if hasattr(user, 'artist'):
        setattr(user.artist, attribute, value)
        user.artist.save()
        setattr(user.producer, attribute, value)
        user.producer.save()
        return True
    elif hasattr(user, 'producer'):
        setattr(user.producer, attribute, value)
        user.producer.save()
        return True
    elif hasattr(user, 'musician'):
        setattr(user.musician, attribute, value)
        user.musician.save()
        return True
    elif hasattr(user, 'musicdirector'):
        setattr(user.musicdirector, attribute, value)
        user.musicdirector.save()
        return True
    else:
        return False


class FaqModel(models.Model):
    """
        Modelo do FAQ
        Attrs:
            title: titulo da faq
            description: texto da faq
            importance: numero inteiro que indica a importancia da faq para ordenar a lista
    """
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    importance = models.IntegerField(verbose_name=_('Importance Level'))

    def __str__(self):
        return self.title


class DefaultUser(BaseModel):
    """
        User generico para Artista, Produtor, Dm e Musico
        Attrs:
            user: fk para User do Django
            phone: numero do telefone
            whatsapp: contato do wpp
            accepted_use_terms: boolean que indica se ja aceitou os termos de uso
            address: endereco
            cep: ceṕ
            doc_number: numero do documento (RG ou CPF)
            name: nome (diferente do User padrao)
            email: email (diferente do User padrao)
    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('User'))
    phone = models.CharField(max_length=250, verbose_name=_('Phone Number'))
    whatsapp = models.CharField(max_length=250, verbose_name=_('WhatsApp Contact'))
    accepted_use_terms = models.BooleanField(verbose_name=_('Has accepted the terms of service'), default=False)
    address = models.CharField(max_length=250, verbose_name=_('Address'))
    cep = models.CharField(max_length=10, verbose_name=_('CEP'))
    doc_number = models.CharField(max_length=14, verbose_name=_('Document number'))

    name = models.CharField(max_length=30, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))

    def __str__(self):
        return '{} - {}'.format(self.name, self.email)
        # return '{}'.format(self.name)

    class Meta:
        abstract = True

    def accept_use_terms(self):
        """
            Aceitar os termos de uso
        """
        try:
            self.accepted_use_terms = True
            self.save()
        except FieldError as e:
            return e

    @staticmethod
    def set_consistency_fields(artist, producer, producer_id):
        """
            Quando o user for artista, temos que definir tbm os campos do produtor relacionado
        """
        if producer_id is not None:
            producer.user_id = producer_id
        producer.name = artist.name
        producer.email = artist.email
        producer.phone = artist.phone
        producer.whatsapp = artist.whatsapp
        producer.accepted_use_terms = artist.accepted_use_terms
        producer.address = artist.address
        producer.cep = artist.cep
        producer.doc_number = artist.doc_number
        producer.save()

    def delete(self, using=None, keep_parents=False):
        # try:
        self.user.delete()
        # except Exception:
        #     pass
        super(DefaultUser, self).delete()


class MusicDirector(DefaultUser):
    """
        Modelo do Diretor Musical
        Attrs:
            user: fk para User do Django
            phone: numero do telefone
            whatsapp: contato do wpp
            accepted_use_terms: boolean que indica se ja aceitou os termos de uso
            address: endereco
            cep: ceṕ
            doc_number: numero do documento (RG ou CPF)
            name: nome (diferente do User padrao)
            email: email (diferente do User padrao)
            region: regiao do dm
    """
    region = models.CharField(max_length=150, verbose_name=_('Region'))

    @staticmethod
    def get_all_active_music_directors():
        """
            metodo usado no form de evento para pegar os diretores musicais ativos e listar as regioes disponiveis
            para criacao de eventos
        """
        return MusicDirector.objects.all()


class Musician(DefaultUser):
    """
        Modelo do musico
        Attrs:
            user: fk para User do Django
            phone: numero do telefone
            whatsapp: contato do wpp
            accepted_use_terms: boolean que indica se ja aceitou os termos de uso
            address: endereco
            cep: ceṕ
            doc_number: numero do documento (RG ou CPF)
            name: nome (diferente do User padrao)
            email: email (diferente do User padrao)
            instrument: indica qual instrumento ele toca
            music_directos: fk para o dm do musico
    """
    instrument = models.CharField(verbose_name=_('Instrument'), max_length=15, choices=INSTRUMENTS)
    music_director = models.ForeignKey(verbose_name=_('Music Director'), to=MusicDirector, on_delete=models.PROTECT)

    # def __str__(self):
    #     return self.get_instrument_display()

    @classmethod
    def set_musician_and_user(cls, form):
        """
            Faz o tratamento do objeto User relacionado para criar/editar o musico
        """
        if form.get('musician_id', None):
            musician = cls.objects.get(id=form.get('musician_id'))
        else:
            musician = cls()
        musician.music_director_id = form['music_director_id']

        musician.name = form['name']
        musician.phone = form['phone']
        musician.whatsapp = form['whatsapp']
        musician.instrument = form['instrument']
        musician.email = form['email']
        # musician.user.first_name = form['name']

        # lidando com usuario
        # if hasattr(musician, 'user'):
        #     musician.user.email = form['email']
        #     musician.user.username = form['email']
        #     musician.user.first_name = form['name']
        #     musician.user.save()
        # else:
        #     import uuid
        #     musician.user = User.objects.create(
        #         username=form['email'],
        #         email=form['email'],
        #         password=uuid.uuid4(),
        #         first_name=form['name']
        #     )

        musician.save()
        return musician


class Producer(DefaultUser):
    """
        Modelo do Produtor
        Attrs:
            user: fk para User do Django
            phone: numero do telefone
            whatsapp: contato do wpp
            accepted_use_terms: boolean que indica se ja aceitou os termos de uso
            address: endereco
            cep: ceṕ
            doc_number: numero do documento (RG ou CPF)
            name: nome (diferente do User padrao)
            email: email (diferente do User padrao)
    """

    def asd(self):
        return self.objects.filter(user__artist__isnull=False)

    # def get_absolute_url(self):
    #     return '/core/producer/{}/change/'.format(self.id)
    pass


class Artist(DefaultUser):
    """
        Modelo do Artista
        Attrs:
            user: fk para User do Django
            phone: numero do telefone
            whatsapp: contato do wpp
            accepted_use_terms: boolean que indica se ja aceitou os termos de uso
            address: endereco
            cep: ceṕ
            doc_number: numero do documento (RG ou CPF)
            name: nome (diferente do User padrao)
            email: email (diferente do User padrao)
            accept_v: boolean que indica se o artista aceita violao
            accept_g: boolean que indica se o artista aceita guitarra
            accept_b: boolean que indica se o artista aceita baixo
            accept_t: boolean que indica se o artista aceita teclado
            accept_bt: boolean que indica se o artista aceita bateria
            accept_bvt: boolean que indica se o artista aceita backing vocal tenor
            accept_bvs: boolean que indica se o artista aceita backing vocal soprano
            accept_bvc: boolean que indica se o artista aceita backing vocal contralto
    """
    accept_v = models.BooleanField(verbose_name=_('Accept Guitar'), default=True)
    accept_g = models.BooleanField(verbose_name=_('Accept Eletric Guitar'), default=True)
    accept_b = models.BooleanField(verbose_name=_('Accept Bass'), default=True)
    accept_t = models.BooleanField(verbose_name=_('Accept Keyboard'), default=True)
    accept_bt = models.BooleanField(verbose_name=_('Accept Drums'), default=True)
    accept_bvt = models.BooleanField(verbose_name=_('Accept Backing Vocal (Tenor)'), default=True)
    accept_bvs = models.BooleanField(verbose_name=_('Accept Backing Vocal (Soprano)'), default=True)
    accept_bvc = models.BooleanField(verbose_name=_('Accept Backing Vocal (Contralto)'), default=True)


class Event(BaseModel):
    """
        Modelo do Evento
        Attrs:
            is_active: indica se o evento foi cancelado. default: true
            name: nome do evento
            region: indica a regiao do evento (ligado diretamente a regiao do dm)
            date: data do evento
            event_time: horario do evento
            event_type: indica o tipo do evento (dentre as opcoes da lista)
            presentation_date: dia da passagem de som
            presentation_time: horario da passagem de som
            artist: artista do evento
            producer: contratante do evento
            music_director: diretor musical do evento
            confirmed: indica se o dm confirmou presenca no evento
            artist_confirmation: indica se o artista confirmou presenca no evento
            notes: observacoes feitas pelo contratante ao criar o evento
            payment_date: data em que o contratante pagou pelo evento
            invoice_number: numero da nota fiscal do pagamento
            payment_method: metodo de pagamento (dentre as opcoes da lista)
            is_finalized: indica se o evento ja foi concluido pelo contratante (apos ele ter ocorrido)
            paid_ammount: indica a quantia paga pelo contratante
            dm_payment_received: quantia recebida pelo dm
            dm_fee: preco pelos servicos do dm
            platform_payment_received: quantia recebida pela plataforma
            platform_fee: preco pelos servicos da plataforma
            total_musicians_fee: preco pelos servicos dos musicos
            total_musicians_transportation_fee: preco do frete dos musicos (depende da distancia ate o centro da cidade)
            total_musicians_payment_received: quantia recebida pelos musicos
            address: endereco do evento
            cep: cep do evento
            distance_from_downtown: distancia do local do evento ate o centro da cidade
            dm_rate: nota do diretor musical neste evento
            payment_allocated: indica se o pagamento ja foi distribuido devidamente entre as partes envolvidas
            attendants_list_ok: indica se o contratante ja confirmou a participacao de todos os musicos
            event_alright: indica se o evento correu bem (informado pelo contratante ao finalizar o evento)
            post_event_comments: comentarios feitos pelo contratante ao finalizar o evento
    """
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'), help_text=_(
        'If for some reason the producer cancels the event, this field will be unmarked'))
    name = models.CharField(max_length=250, verbose_name=_('Event name'))
    region = models.TextField(verbose_name=_('Region'))
    date = models.DateField(verbose_name=_('Event Date'))
    event_time = models.TimeField(verbose_name=_('Event Time'))
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='Show', verbose_name=_('Event Type'))
    presentation_date = models.DateField(verbose_name=_('Rehearsal Date'))
    presentation_time = models.TimeField(verbose_name=_('Rehearsal Time'))
    artist = models.ForeignKey(to=Artist, on_delete=models.PROTECT, null=True, verbose_name=_('Artist'))
    producer = models.ForeignKey(to=Producer, on_delete=models.PROTECT, verbose_name=_('Producer'))
    music_director = models.ForeignKey(to=MusicDirector, on_delete=models.PROTECT, null=True,
                                       verbose_name=_('Music Director'))
    confirmed = models.CharField(default='PE', max_length=10, choices=EVENT_STATUSES,
                                 verbose_name=_('Music Director Confirmation'))  # Confirmacao do DM
    artist_confirmation = models.CharField(default='PE', max_length=10,
                                           choices=EVENT_STATUSES,
                                           verbose_name=_('Artist Confirmation'))  # Confirmacao do artista
    notes = models.TextField(null=True, blank=True, verbose_name=_('Event Notes'))

    payment_date = models.DateField(blank=True, null=True, verbose_name=_('Payment Date'))
    invoice_number = models.CharField(blank=True, null=True, verbose_name=_('Invoice Number'), max_length=250)
    payment_method = models.CharField(default='DD', verbose_name=_('Payment Method'), max_length=2,
                                      choices=PAYMENT_METHODS)
    is_finalized = models.BooleanField(verbose_name=_('Event has been finalized'), default=False)

    paid_ammount = models.FloatField(blank=True, null=True, verbose_name=_('Paid ammount'))
    dm_payment_received = models.FloatField(verbose_name=_('Music Director Payment Received'), default=0.00)
    # fee = taxa
    dm_fee = models.FloatField(verbose_name=_('Music Director Fee'), default=DEFAULT_PRICES.get('music_director_fee'))
    platform_payment_received = models.FloatField(verbose_name=_('Platform Payment Received'), default=0.00)
    platform_fee = models.FloatField(verbose_name=_('Platform Fee'), default=DEFAULT_PRICES.get('platform_fee'))
    total_musicians_fee = models.FloatField(verbose_name=_('Total Musicians Fee'), default=0.00)
    total_musicians_transportation_fee = models.FloatField(verbose_name=_('Total Musicians Transportation Fee'),
                                                           default=0.00)
    total_musicians_payment_received = models.FloatField(verbose_name=_('Total Musicians Payment Received'),
                                                         default=0.00)
    address = models.CharField(max_length=250, verbose_name=_('Address'))
    cep = models.CharField(max_length=10, verbose_name=_('CEP'))
    distance_from_downtown = models.PositiveIntegerField(verbose_name=_('Distance from Downtown (in Km)'),
                                                         validators=[MinValueValidator(0), MaxValueValidator(150)],
                                                         help_text=_('You can create events up to 150km from downtown'),
                                                         default=0)
    dm_rate = models.PositiveIntegerField(verbose_name=_('Music Director Rate'),
                                          help_text=_('The Music Director rate is the mean of his musicians rates'),
                                          default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    payment_allocated = models.BooleanField(verbose_name=_('Payment has been allocated'), default=False)
    attendants_list_ok = models.BooleanField(verbose_name=_('All the attendants have been listed'), default=False)
    # todo nao estamos usando essa variavel por enquanto
    event_alright = models.CharField(verbose_name=_('Everything Went OK'), max_length=2, choices=EVENT_ALRIGHT_CHOICES,
                                     default='NA')
    post_event_comments = models.TextField(verbose_name=_('Say something about this event overall'), blank=True,
                                           null=True)

    def __str__(self):
        return '{name}'.format(name=self.name)

    def services_fee(self):
        """
            retorna o preco total dos servicos
            preco dm + preco plataforma + preco dos musicos
        """
        return self.dm_fee + self.platform_fee + self.total_musicians_fee

    def has_happened(self):
        """
            Indica se a data do evento passou e se o artista e diretor musical haviam confirmado a presenca
        """
        return self.is_past() and self.is_confirmed() and self.is_artist_confirmed()

    def is_past(self):
        """
            indica se a data do evento passou
        """
        return date.today() > self.date

    def is_confirmed(self):
        """
            indica se o diretor musical ja confirmou participacao
        """
        return self.confirmed == self.get_confirmed_status_code()

    def is_artist_confirmed(self):
        """
            indica se o artista ja confirmou participacao
        """
        return self.artist_confirmation == self.get_confirmed_status_code()

    def artist_is_producer(self):
        """
            indica se o artista do evento tambem eh o seu contratante
        """
        return self.artist.user == self.producer.user

    def total_price(self):
        """
            retorna o preco total do evento
            Preco do evento = taxa dm + taxa plataforma + taxa musicos + frete musicos
        """
        return self.dm_fee + self.platform_fee + self.total_musicians_fee + self.total_musicians_transportation_fee

    def event_price_calculator(self):
        """
            Calcula os precos relativos ao evento. O preco total eh calculado dinamicamente toda vez que eh chamado
            Os precos relativos a cada parte, POR AGORA se encontram no dict DEFAULT_PRICES do settings.
        """
        self.platform_fee = DEFAULT_PRICES.get('platform_fee')
        self.dm_fee = DEFAULT_PRICES.get('music_director_fee')
        main_musician_fee = DEFAULT_PRICES.get('main_musician_fee')
        sub_musician_fee = DEFAULT_PRICES.get('sub_musician_fee')
        # se nao tem parent, eh principal. e vice versa
        total_main_musicians = MusicianEvent.objects.filter(event_id=self.id,
                                                            parent_musician_event__isnull=True).count()
        total_sub_musicians = MusicianEvent.objects.filter(event_id=self.id,
                                                           parent_musician_event__isnull=False).count()
        main_musicians_total_fee = main_musician_fee * total_main_musicians
        sub_musicians_total_fee = sub_musician_fee * total_sub_musicians
        self.total_musicians_transportation_fee = self.get_transportation_fee()
        self.total_musicians_fee = main_musicians_total_fee + sub_musicians_total_fee
        # self.total_price = platform_fee + dm_fee + main_musicians_total_fee + sub_musicians_total_fee
        self.save()

    def get_transportation_fee(self):
        """
            pega a taxa do frete dos musicos. feito em uma funcao diferente porque futuramente isto sera dinamico.
            se a distancia do centro for maior que 20km, a cada 1km adicionaremos um valor fixo de frete
        """
        # pega o numero de instrumentistas que irao ao evento
        num_musicians = MusicianEvent.objects.filter(event_id=self.id, parent_musician_event__isnull=True).count()
        if self.distance_from_downtown > 20:
            # valor = frete * distancia total - 20 (valor "gratuito" de distancia) p cada instrumentista
            return DEFAULT_PRICES.get('extra_distance_fee') * (self.distance_from_downtown - 20) * num_musicians
        else:
            return 0.00

    @staticmethod
    def pay_musicians(event_musicians):
        """
            paga os musicos um a um de acordo com a lista de presenca e taxa de transporte.
            retorna o valor total pago para calculo do preco total no metodo responsavel por concluir o evento
            Args:
                event_musicians: QuerySet
        """
        total = 0
        for musician in event_musicians:
            # sou principal e fui
            if musician.attended and not musician.parent_musician_event:
                musician.musician_payment_received = DEFAULT_PRICES.get(
                    'main_musician_fee') + musician.musician_transportation_fee
            elif musician.parent_musician_event:
                main_musician = MusicianEvent.objects.get(id=musician.parent_musician_event_id)
                # sou sub e o principal foi
                if main_musician.attended:
                    # recebo so a taxa de sub. sem taxa de frete
                    musician.musician_payment_received = DEFAULT_PRICES.get('sub_musician_fee')
                # sou sub, fui, e o principal nao foi
                elif not main_musician.attended and musician.attended:
                    # recebo a quantia do principal, a taxa de sub, e a taxa de frete
                    musician.musician_payment_received = DEFAULT_PRICES.get('sub_musician_fee') + DEFAULT_PRICES.get(
                        'main_musician_fee') + musician.musician_transportation_fee
            total += musician.musician_payment_received
            musician.save()
        return total

    @staticmethod
    def dm_rate_calculator(event_musicians):
        """
            calcula a nota recebida pelo diretor musical no evento
            nota dm = media das notas recebidas pelos musicos
            Args:
                event_musicians: QuerySet
        """
        total_rate = 0
        total_musicians = 0
        for musician in event_musicians:
            if musician.musician_rate:
                total_rate += musician.musician_rate
                total_musicians += 1
        return total_rate / total_musicians

    def conclude_event(self):
        """
            conclui o evento, definindo as variaveis importantes para tal
        """
        # o evento ja tem que ter acontecido para ser finalizado
        if not self.has_happened():
            raise Exception
        self.is_finalized = True
        # paid_ammount = self.paid_ammount
        self.dm_payment_received = self.dm_fee
        # paid_ammount -= DEFAULT_PRICES.get('music_director_fee')
        self.platform_payment_received = self.platform_fee
        # paid_ammount -= DEFAULT_PRICES.get('platform_fee')
        event_musicians = MusicianEvent.objects.filter(event=self)
        self.total_musicians_payment_received = self.pay_musicians(event_musicians)
        # paid_ammount -= self.total_musicians_payment_received
        self.dm_rate = self.dm_rate_calculator(event_musicians)
        self.payment_allocated = True
        self.attendants_list_ok = True
        self.save()

    # inicio dos metodos default para obtencao de codigos
    @staticmethod
    def get_confirmed_status_code():
        return 'YES'

    @staticmethod
    def get_refused_status_code():
        return 'NO'

    @staticmethod
    def get_pending_status_code():
        return 'PE'

    @staticmethod
    def get_event_alright_success_code():
        return 'OK'

    @staticmethod
    def get_event_alright_fail_code():
        return 'NO'

    @staticmethod
    def get_event_alright_pending_code():
        return 'NA'

    # termino dos metodos default para obtencao de codigos

    @classmethod
    def get_status_code_icon_html(cls, status_code):
        """
            retorna o icone html que indica o status de confirmacao
            Args:
                status_code: string
        """
        if status_code == cls.get_confirmed_status_code():
            return '<span class="fa fa-check-circle text-success"></span>'
        elif status_code == cls.get_refused_status_code():
            return '<span class="fa fa-times-circle text-danger"></span>'
        else:
            return '<span class="fa fa-clock-o text-warning"></span>'

    # inicio dos metodos de pegar o icone html para indicacao de confirmacao de algo
    def get_confirmed_icon_html(self):
        return self.get_status_code_icon_html(self.confirmed)

    def get_artist_confirmation_icon_html(self):
        return self.get_status_code_icon_html(self.artist_confirmation)

    def get_payment_confirmation_icon_html(self):
        if self.paid_ammount:
            return self.get_status_code_icon_html(self.get_confirmed_status_code())
        else:
            return self.get_status_code_icon_html(self.get_pending_status_code())

    # termino dos metodos de pegar o icone html para indicacao de confirmacao de algo

    def get_happened_status(self):
        """
            retorna uma string para indicar o estado do evento na lista de eventos passados
        """
        from django.utils.html import format_html
        if self.has_happened() and not self.is_finalized:
            return format_html('{} {}'.format(_('Confirmation Pending'), self.get_status_code_icon_html(self.get_pending_status_code())))
        elif self.has_happened() and self.is_finalized:
            return format_html('{} {}'.format(_('Concluded'), self.get_status_code_icon_html(self.get_confirmed_status_code())))
        elif (self.is_past() and self.event_alright == self.get_event_alright_fail_code()) or (
                self.is_past() and self.is_active):
            return format_html('{} {}'.format(_('Did not happen'), self.get_status_code_icon_html(self.get_refused_status_code())))
        elif not self.is_active:
            return format_html('{} {}'.format(_('Canceled'), self.get_status_code_icon_html(self.get_refused_status_code())))

    def get_confirmed_is_pending(self):
        """
            verifica se o diretor musical ja confirmou participacao
        """
        return self.confirmed == self.get_pending_status_code()

    def get_artist_confirmation_is_pending(self):
        """
            verifica se o artista ja confirmou participacao
        """
        return self.artist_confirmation == self.get_pending_status_code()

    def get_everyone_declined(self):
        """
            se o dm e o artista tiverem recusado participacao no evento, retorna true
        """
        return self.artist_confirmation == self.get_refused_status_code() and self.confirmed == self.get_refused_status_code()

    @classmethod
    def create_event_and_musician_event(cls, form):
        """
            metodo responsavel por criar o evento e seus musician events vazios correspondentes
        """
        event = cls()
        event.name = form['name']
        event.region = MusicDirector.objects.get(id=form['music_director_id']).region
        event.music_director_id = form['music_director_id']
        event.date = form['date']
        event.event_time = form['event_time']
        event.presentation_date = form['presentation_date']
        event.presentation_time = form['presentation_time']
        event.event_type = form['event_type']
        event.artist = form['artist']
        event.producer_id = form['producer_id']
        event.notes = form['notes']
        event.address = form['address']
        event.cep = form['cep']
        event.distance_from_downtown = form['distance']
        event.save()

        for instrument in form.get('instruments'):
            main_musician = MusicianEvent.objects.create(event=event, instrument=instrument)
            # cria musician event para os musicos substitutos
            MusicianEvent.objects.create(event=event, instrument=instrument, parent_musician_event=main_musician)

        return event


class AbstractSong(BaseModel):
    """
        Modelo de referencia abstrata. Tanto artista como evento tem referencias; porem sao distintas.
        Attrs:
            name: nome da referencia
            file: arquivo
            links: links
            notes: observacoes
    """
    class Meta:
        abstract = True

    name = models.CharField(verbose_name=_('Name'), max_length=20, help_text=_('Identify this reference'))
    file = models.FileField(verbose_name=_('File'), upload_to='uploads/artist_references', blank=True, null=True)
    links = models.CharField(verbose_name=_('Links'), max_length=255, blank=True, null=True)
    notes = models.TextField(verbose_name=_('Notes'))

    def __str__(self):
        return '{name}'.format(name=self.name)

    @classmethod
    def set_song_and_artist_base(cls, form, extras):
        # checando se tem id, o que quer dizer put e atualiza o modelo correto
        if form.get('reference_id', None):
            song = cls.objects.get(id=form.get('reference_id'))
        else:
            song = cls()

        song.name = form['name']
        if form['file']:
            song.file = form['file']
        else:
            song.file = None
        song.notes = form['notes']
        song.links = form['links']
        if len(extras) > 0:
            for extra in extras:
                if form.get(extra, None):
                    setattr(song, extra, form[extra])
        song.save()
        return song


class ArtistSong(AbstractSong):
    """
        Referencias cadastradas pelo artista. o Diretor tem acesso a elas.
        Attrs:
            artist: artista dono da referencia
    """
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE, verbose_name=_('Artist'))

    @classmethod
    def set_song_and_artist(cls, form):
        return cls.set_song_and_artist_base(form, ('artist_id',))


class EventSong(AbstractSong):
    """
        Referencias do evento. O Diretor as cadastra e os músicos tem acesso a elas.
        Attrs:
            artist: artista dono da referencia
    """
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, verbose_name=_('Event'))

    @classmethod
    def set_song_and_artist(cls, form):
        return cls.set_song_and_artist_base(form, ('event_id',))


class MusicianEvent(BaseModel):
    """
        Modelo MusicianEvent responsavel por fazer o relacionamento do musico com o evento
        Attrs:
            event: evento relacionado
            musician: musico relacionado
            instrument: instrumento desse musico
            confirmation: indica se o musico atribuido confirmou participacao
            musician_fee: preco do musico em questao
            musician_transportation_fee: preco do transporte do musico
            musician_payment_received: pagamento recebido pelo musico ao final do evento
            musician_rate: nota do musico
            parent_musician_event: indica se o musico eh substituto e, se sim, quem eh o seu principal
            attended: indica se o musico compareceu ao evento
    """
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, verbose_name=_('Event'))
    musician = models.ForeignKey(verbose_name=_('Musician'), to=Musician, on_delete=models.CASCADE, null=True)
    instrument = models.CharField(verbose_name=_('Instrument'), max_length=15, choices=INSTRUMENTS)
    confirmation = models.CharField(verbose_name=_('Musician Confirmation'), default='PE', max_length=10,
                                    choices=EVENT_STATUSES)  # Confirmacao do musico
    musician_fee = models.FloatField(verbose_name=_('Musician Fee'), default=0.00)
    musician_transportation_fee = models.FloatField(verbose_name=_('Musician Transportation Fee'), default=0.00)
    musician_payment_received = models.FloatField(verbose_name=_('Musician Payment'), default=0.00)
    musician_rate = models.PositiveIntegerField(verbose_name=_('Musician Rate'), null=True, blank=True,
                                                validators=[MinValueValidator(0), MaxValueValidator(5)])
    parent_musician_event = models.ForeignKey(to='self', verbose_name=_('Main musician'),
                                              on_delete=models.CASCADE, null=True, blank=True)
    attended = models.BooleanField(verbose_name=_('Musician Has Attended'), default=False)

    def transportation_fee_calculator(self):
        """
            calcula o preco do frete do musico
        """
        return DEFAULT_PRICES.get('extra_distance_fee') * (
                Event.objects.get(id=self.event_id).distance_from_downtown - 20)

    @classmethod
    def set_musician(cls, form):
        """
            define o musico do musician_event
        """
        musician_event = cls()
        musician_event.musician = form['musician']
        musician_event.save()
        return musician_event

    def instrument_for_humans(self):
        """
            retorna de maneira legivel o nome do instrumento do musico, assim como informa se ele eh substituto
            ou principal
        """
        if self.parent_musician_event_id is not None:
            return "(Sub.) {}".format(self.get_instrument_display())
        else:
            return self.get_instrument_display()

    def __str__(self):
        """
            O nome mostrado no admin indicará o evento, o instrumento necessario, e, caso o espaco pro musico ja tenha
            sido preenchido, mostra o nome dele, e do contrário, mostra None.
        """
        return '{self.event} - {self.instrument} : {self.musician}'.format(self=self)

    class Meta:
        """
            um musico em um evento nao podem se repetir
        """
        unique_together = [['musician', 'event']]


class Comment(models.Model):
    """
        Modelo para troca de mensagens (comentarios) entre o DM e o artista
        Attrs:
            event: evento relacionado
            author: quem fez o comentario
            message: conteudo do comentario
            created_date: data de criacao
    """
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, verbose_name=_('Event'))
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('Author'))
    message = models.TextField(verbose_name=_('Message'))
    created_date = models.DateTimeField(verbose_name=_('Created Date'))

    def __str__(self):
        return self.message[:20]

    def date_time_pretty(self):
        """
            retorna a data de criacao de maneira mais legivel para o front
        """
        return self.created_date.strftime('%Y-%m-%d at %H:%M')

    @classmethod
    def set_new_comment(cls, form):
        """
            metodo responsavel por criar um novo comentario
        """
        comment = cls()
        comment.author_id = form['author_id']
        comment.created_date = form['created_date']
        comment.event_id = form['event_id']
        comment.message = form['message']
        comment.save()
        return comment


@receiver(post_save, sender=MusicianEvent)
def musician_event_post_save(sender, instance, created, *args, **kwargs):
    """
        Post save do MusicianEvent. Envia email quando um musico eh atribuido a uma posicao, e quando o objeto
        eh criado, atribui as variaveis de preco do musico e da taxa de transporte
    """
    if not created and hasattr(instance, 'musician') and not instance.attended:
        from post_office import mail
        try:
            mail.send(
                instance.musician.user.email,
                subject='{}'.format(_('New event 2 u!')),
                html_message='{}.<br > {} <a href="http://guigyou.xyz/app/event/{}/">{}</a> {}.'.format(
                    _('You have been added to a new event'), _('Click'), instance.event_id, _('here'), _('to see')),
            )
        except AttributeError:
            pass
    elif created:
        if instance.parent_musician_event:
            instance.musician_fee = DEFAULT_PRICES.get('sub_musician_fee')
        else:
            instance.musician_fee = DEFAULT_PRICES.get('main_musician_fee')
        instance.musician_transportation_fee = instance.transportation_fee_calculator()
        instance.save()


@receiver(post_save, sender=Artist)
def artist_post_save(sender, instance, created, *args, **kwargs):
    default_user_post_save(sender, instance, created, True, False, *args, **kwargs)


@receiver(post_save, sender=Musician)
def musician_post_save(sender, instance, created, *args, **kwargs):
    default_user_post_save(sender, instance, created, *args, **kwargs)


@receiver(post_save, sender=Producer)
def producer_post_save(sender, instance, created, *args, **kwargs):
    default_user_post_save(sender, instance, created, False, True, *args, **kwargs)


@receiver(post_save, sender=MusicDirector)
def music_director_post_save(sender, instance, created, *args, **kwargs):
    default_user_post_save(sender, instance, created, *args, **kwargs)


def default_user_post_save(sender, instance, created, is_artist=False, is_producer=False, *args, **kwargs):
    """
        Cria um objeto user a partir do defaultUser com senha aleatoria. Envia email para novos usuarios.
        No caso de artista, define os campos do objeto produtor associado a ele para garantir consistencia.
    """
    if created and (not hasattr(instance, 'user') or instance.user is None):
        import uuid
        from django.db import IntegrityError
        try:
            user = User.objects.create(first_name=instance.name, email=instance.email, username=instance.email,
                                       password=uuid.uuid4())
        except IntegrityError:
            raise IntegrityError
        user.save()
        instance.user_id = user.id
        instance.save()
        from post_office import mail
        mail.send(
            instance.email,
            subject='{}'.format(_('Welcome to Gig2You!')),
            html_message='{}.<br > {}. <br><br><br>{}.'.format(
                _('Welcome to the Gig2You platform! We hope you have a nice time around here =)'),
                _('Please visit our website at www.gig2you.com and reset your password to start using our platform'),
                _('If you have received this email by mistake, simply ignore it. We are sorry for the inconvenience')),
        )

    else:
        user = User.objects.get(id=instance.user_id)
        user.first_name = instance.name
        user.email = instance.email
        user.username = instance.email
        user.save()
    # if the user is an artist, we have to update his producer object fields, too
    if is_artist:
        # if he doesnt have a producer object attached yet, create a new one and set its id
        if not hasattr(user, 'producer') or user.producer is None:
            producer = Producer()
            producer_id = user.id
        else:
            producer = user.producer
            producer_id = None
        # sets the artist-producer fields to ensure consistency
        DefaultUser.set_consistency_fields(artist=instance, producer=producer, producer_id=producer_id)

    # elif is_producer:
    #     if hasattr(user, 'artist'):
    #         artist = user.artist
    #         artist.name = instance.name
    #         artist.email = instance.email
    #         artist.phone = instance.phone
    #         artist.whatsapp = instance.whatsapp
    #         artist.save()
