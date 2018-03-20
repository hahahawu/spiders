import json

import msgpack
from kafka import KafkaProducer
from kafka.client import log
from kafka.errors import KafkaError

producer = KafkaProducer(value_serializer=msgpack.dumps, bootstrap_servers=['master:9092'])
for x in range(20):
    producer.send('test', {'key' + str(x): 'value' + str(x)})

# Asynchronous by default
future = producer.send('test', b'testiik')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)

# # produce keyed messages to enable hashed partitioning
# producer.send('test', key=b'foo', value=b'bar')
#
# # encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps, bootstrap_servers=['master:9092'])
# producer.send('test', {'key': 'value'})
#
# # produce json messages
# producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=['master:9092'])
# producer.send('test', {'key': 'value'})
#
# # configure multiple retries
# producer = KafkaProducer(retries=5, bootstrap_servers=['master:9092'])

producer.flush()
producer.close(timeout=10)
