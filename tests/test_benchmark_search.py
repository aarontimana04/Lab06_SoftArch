import pytest
from papers_api.search_engine import search 
@pytest.mark.django_db  
def test_search_performance(benchmark):
    # Definir una query
    query = "inteligencia artificial aprendizaje automático"

    # Usa pytest-benchmark para medir el tiempo promedio de ejecución
    result = benchmark(lambda: search(query))

    # Validar que devuelva resultados
    assert isinstance(result, tuple)
    assert len(result) >= 2  # (sliced, total)
