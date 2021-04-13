import datetime
from flask import jsonify
from schemas import CompanySchema
from models import Company

company_schema = CompanySchema()


# returns company data for contact info
def get_one(comp_id: int):
    company = Company.query.filter_by(comp_id=comp_id).first()
    if company:
        result = company_schema.dump(company)
        return jsonify(result)
    else:
        return jsonify(message="Company not found"), 404
