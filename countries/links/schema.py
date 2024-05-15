
import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from links.models import Country, Vote
from graphql import GraphQLError
from django.db.models import Q
from .models import Country


class CountryType(DjangoObjectType):
    class Meta:
        model = Country

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    countries = graphene.List(CountryType, search=graphene.String())
    votes = graphene.List(VoteType)

    def resolve_countries(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search) |
                Q(language__icontains=search)
            )
            return Country.objects.filter(filter)

        return Country.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

   

class CreateCountry(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    capital = graphene.String()
    population = graphene.Int()
    language = graphene.String()

    class Arguments:
        name = graphene.String()
        capital = graphene.String()
        population = graphene.Int()
        language = graphene.String()


    def mutate(self, info, name, capital, population, language):
        user = info.context.user or None

        country = Country(
            name=name,
            capital=capital,
            population=population,
            language=language
        )
        country.save()

        return CreateCountry(
            id=country.id,
            name=country.name,
            capital=country.capital,
            population=country.population,
            language=country.language
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    country = graphene.Field(CountryType)

    class Arguments:
        country_id = graphene.Int()

    def mutate(self, info, country_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')


        country = Country.objects.filter(id=country_id).first()
        if not country:
            raise Exception('Invalid COUNTRYYYY!')

        Vote.objects.create(
            user=user,
            country=country,
        )

        return CreateVote(user=user, country=country)

#4
class Mutation(graphene.ObjectType):
    create_country = CreateCountry.Field()
    create_vote = CreateVote.Field()


