import json
import pytest
import hashlib

from faker import Faker

from app.utils.xml import parse_xml, generate_hash  # ajuste conforme seu projeto


faker = Faker()


class TestParseXML:
    def parse_xml_success_test(self):
        article_id = faker.uuid4()
        article_title = faker.sentence()

        xml_content = f"<?xml version='1.0'?><article id='{article_id}' title='{article_title}' />".encode("utf-8")

        assert parse_xml(xml_content, "test_file.xml") == {
            "id": article_id,
            "title": article_title,
        }

    def parse_xml_failure_test(self):
        xml_content = b"<?xml version='1.0'?><root><item>Nothing here</item></root>"

        with pytest.raises(ValueError) as exc_info:
            parse_xml(xml_content, "invalid_file.xml")

        assert "No <article> element found" in str(exc_info.value)


class TestGenerateHash:
    def generate_hash_success_test(self):
        data = {
            "id": faker.uuid4(),
            "title": faker.sentence(),
        }

        assert (
            generate_hash(data) == hashlib.sha256(
                json.dumps(data).encode("utf-8")
            )
            .hexdigest()
        )

    def generate_hash_failure_test(self):
        data = {
            "id": faker.uuid4(),
            "title": faker.sentence()
        }

        assert (
            generate_hash(data) != hashlib.sha256(
                json.dumps({"id": faker.uuid4(), "title": faker.sentence()}).encode("utf-8")
            )
            .hexdigest()
        )
