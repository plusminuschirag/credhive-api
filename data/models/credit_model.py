from mongoengine import Document, StringField, IntField, FloatField, URLField, EmailField, DateField


class Credit(Document):
    CIN = StringField(required=True, unique=True)
    company_name = StringField(required=True)
    address = StringField(required=True)
    registration_date = DateField(required=True)  # Store as string or use DateTimeField
    number_of_employees = IntField(required=True)
    raised_capital = FloatField(required=True)
    turnover = FloatField(required=True)
    net_profit = FloatField(required=True)
    contact_number = StringField(required=True)
    contact_email = EmailField(required=True)
    company_website = URLField(required=True)
    loan_amount = FloatField(required=True)
    loan_interest_percentage = FloatField(required=True)
    account_status = StringField(required=True)


class CreditModel:
    @staticmethod
    def get_all_credits():
        credits = Credit.objects.all()
        credit_dicts = []
        for credit in credits:
            credit_dict = (
                credit.to_mongo().to_dict()
            )  # Converting to dict, experiment shows pydantic and mongo having different handling of data types.
            # Remove the '_id' field
            credit_dict.pop("_id", None)  # If there are other fields to remove, do similarly
            credit_dicts.append(credit_dict)
        return credit_dicts

    @staticmethod
    def get_id_credit(id):
        credit = Credit.objects(CIN=id).first()
        if credit:
            credit_dict = credit.to_mongo().to_dict()
            credit_dict.pop("_id", None)
            return credit_dict
        return None

    @staticmethod
    def save_credit(credit_data):
        existing_credit = Credit.objects(CIN=credit_data.CIN).first()
        if existing_credit:
            return False, "Credit with this CIN already exists"

        # Convert Pydantic URL to string
        credit_data.company_website = str(credit_data.company_website)
        credit = Credit(**credit_data.dict())
        credit.save()
        return True, "Credit saved successfully"

    @staticmethod
    def update_credit_data(id, credit_data):
        credit = Credit.objects(CIN=id).first()
        print(credit)
        if credit:
            credit.update(**credit_data.dict(exclude_none=True))
            return True
        return False

    @staticmethod
    def delete_credit_by_id(id):
        credit = Credit.objects(CIN=id).first()
        if credit:
            credit.delete()
            return True
        return False
