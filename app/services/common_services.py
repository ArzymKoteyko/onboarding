def partition_to_dict(partition):
    return {col.name: getattr(partition, col.name) for col in partition.__table__.columns}

