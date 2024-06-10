# swaggerTransformer
make wiremock mapper out of swagger file


# Example command to start WireMock standalone
java -jar wiremock-standalone-{version}.jar --port 8080 --root-dir ./wiremock


curl -X POST --data @mappings/mapping_0.json http://localhost:8080/__admin/mappings


python -m unittest test_swaggerTransformer.py


docker build -t wiremock-mappings .

docker run -p 8080:8080 wiremock-mappings
