import pytest

from app import db
from app.features.auth.models import User
from app.features.dataset.models import BaseDataset, DSMetaData, GameDataset, GameDatasetFile, PublicationType

pytestmark = pytest.mark.repository


@pytest.mark.parametrize("names", [("games.csv",), ("games.csv", "reviews.csv")])
def test_game_dataset_persists_csv_files_and_metadata(test_app, clean_database, names):
    with test_app.app_context():
        owner = User(email="owner@example.com", password="secret")
        db.session.add(owner)
        db.session.flush()

        dataset = GameDataset(
            user_id=owner.id,
            ds_meta_data=DSMetaData(
                title="Steam games",
                description="Steam dataset",
                publication_type=PublicationType.NONE,
                tags="steam",
            ),
            files=[GameDatasetFile(name=name, checksum="abc", size=42) for name in names],
        )
        db.session.add(dataset)
        db.session.flush()
        dataset_id = dataset.id
        owner_id = owner.id
        db.session.commit()
        db.session.expunge_all()

        stored = db.session.get(GameDataset, dataset_id)
        assert isinstance(stored, BaseDataset)
        assert stored.user_id == owner_id
        assert stored.ds_meta_data.title == "Steam games"
        assert sorted(file.name for file in stored.files) == sorted(names)
        assert all(file.game_dataset_id == dataset_id for file in stored.files)
