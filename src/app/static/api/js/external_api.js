const get_all_external_api_collections = async (success, fail) => {
  const options = { method: 'GET', headers: { accept: '*/*', 'x-api-key': 'demo-api-key' } };
  const response = await fetch('https://api.reservoir.tools/search/collections/v1', options);
  const rjson = await response.json();
  if (response.status === 200) {
    success(rjson);
  } else {
    console.log('fail ', response);
    fail();
  }
}

const get_all_external_api_tokens = async (collectionId, success, fail) => {
  const options = { method: 'GET', headers: { accept: '*/*', 'x-api-key': 'demo-api-key' } };
  const response = await fetch(`https://api.reservoir.tools/tokens/v5?collection=${collectionId}`, options);
  const rjson = await response.json();
  if (response.status === 200) {
    success(rjson);
  } else {
    console.log('fail ', response);
    fail();
  }
}