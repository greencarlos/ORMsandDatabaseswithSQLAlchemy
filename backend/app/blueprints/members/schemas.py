from app.extensions import ma
from app.models import Member

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        include_relationships = False


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
login_schema = MemberSchema(exclude=['name', 'DOB'])
