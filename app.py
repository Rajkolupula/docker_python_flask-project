from flask import Flask
import os

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# -----------------------------
# OpenTelemetry Configuration
# -----------------------------

resource = Resource(attributes={
    SERVICE_NAME: "flask-todo-app"
})

trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",  # Change if needed
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Auto-instrument Flask
FlaskInstrumentor().instrument_app(app)

# -----------------------------
# Flask Routes
# -----------------------------

@app.route("/")
def hello():
    return "Flask inside Docker with OpenTelemetry!!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        debug=True,
        host="0.0.0.0",
        port=port
    )
