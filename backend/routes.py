from flask import Blueprint, jsonify, request

artists_bp = Blueprint("artists", __name__, url_prefix="/api")


def repository_response(result, not_found_message="Resource not found"):
    if isinstance(result, dict) and "error" in result:
        status_code = result.get("statusCode", 500)
        return jsonify(result), status_code

    if result is None:
        return jsonify({"error": not_found_message}), 404

    return jsonify(result)


@artists_bp.get("/artists/search")
def search_artists():
    from backend.repositories import artist_repository

    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({"error": "Search name is required"}), 400

    result = artist_repository.searchForArtist(name)
    return repository_response(result)


@artists_bp.post("/artists/select")
def select_artist():
    from backend.repositories import artist_repository

    artist = request.get_json(silent=True)

    if not isinstance(artist, dict):
        return jsonify({"error": "Artist data is required"}), 400

    if not artist.get("uuid"):
        return jsonify({"error": "Artist UUID is required"}), 400

    result = artist_repository.selectArtist(artist)
    return repository_response(result, "Artist could not be selected")


@artists_bp.get("/artists/<uuid>/cities")
def get_artist_cities(uuid):
    from backend.repositories import artist_audience_repository

    result = artist_audience_repository.getAllArtistCities(uuid)
    return repository_response(result, "No cities found for this artist")


@artists_bp.get("/artists/<uuid>/cities/<int:city_id>/audience")
def get_city_audience(uuid, city_id):
    from backend.repositories import artist_audience_repository

    platform = request.args.get("platform", "spotify")

    result = artist_audience_repository.selectCity(
        artist_uuid=uuid,
        cityId=city_id,
        platform=platform,
    )

    return repository_response(result, "Audience data not found")

@artists_bp.get("/venues/recommend")
def recommend_venues():
    from backend.repositories import venue_repository

    artist_uuid = request.args.get("artist_id", "").strip()
    city_id = request.args.get("city_id", type=int)
    min_capacity = request.args.get("min_capacity", type=int)
    max_capacity = request.args.get("max_capacity", type=int)

    if not artist_uuid or not city_id:
        return jsonify({"error": "artist_id and city_id are required"}), 400

    result = venue_repository.find_best_venues_for_artist(artist_uuid, city_id)
    return repository_response(result, "No venues found for this artist/city")