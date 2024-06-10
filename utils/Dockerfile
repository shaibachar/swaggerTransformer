# Use the official WireMock image as the base image
FROM wiremock/wiremock:latest

# Create a directory for the mappings
RUN mkdir -p /home/wiremock/mappings

# Copy the mappings from the local filesystem to the container
COPY mappings /home/wiremock/mappings

# Expose WireMock port
EXPOSE 8080

# Enable response templating and verbose logging by setting the WireMock options
CMD ["--global-response-templating", "--port", "8080", "--root-dir", "/home/wiremock", "--verbose"]
