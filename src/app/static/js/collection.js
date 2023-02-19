'use strict';

const e = React.createElement;

function App() {

  const [loggedInUsername, setLoggedInUsername] = React.useState(null);
  const [pageLanguage, setPageLanguage] = React.useState("en");
  const [userInfo, setUserInfo] = React.useState(null);
  const [collectionName, setCollectionName] = React.useState("");
  const [allApiCollections, setAllApiCollections] = React.useState([]);
  const [tokenList, setTokenList] = React.useState([]);
  const [tokensInCustomCollection, setTokensInCustomCollection] = React.useState([]);
  const [displayDraggableDiv, setDisplayDraggableDiv] = React.useState(true);
  const [selectedCollection, setSelectedCollection] = React.useState(undefined);

  const collectionId = getCollectionId();
  if (collectionId != null) {
    window.document.title = "Edit Custom Collection";
  }

  const getData = () => {
    add_loading(window.document.body);
    getLoggedInUsername((username) => { setLoggedInUsername(username) });
    getPageLanguage((lang => { setPageLanguage(lang); }));
    get_user_data_api((data) => setUserInfo(data.data));
    var infoObtained = 0;
    get_all_external_api_collections((data) => {
      setAllApiCollections(data.collections);
      const preselectedApiCollectionId = localStorage.getItem('selectedApiCollection');
      if (preselectedApiCollectionId && collectionId && data.collections.filter(c => c.collectionId === preselectedApiCollectionId).length > 0) {
        changeCollectionsSelect(preselectedApiCollectionId, null);
        localStorage.removeItem('selectedApiCollection');
      } else {
        changeCollectionsSelect(data.collections[0].collectionId, null);
      }
      infoObtained += 1;
      if (infoObtained === 2 || collectionId == null) {
        remove_loading();
      }
    }, () => {
      Swal.fire({
        title: 'Collections could not be obtained, reload.',
        text: "",
        icon: 'error',
        timer: 1000,
      });
    });
    if (collectionId != null) {
      get_collection_info_api(collectionId, (data) => {
        setCollectionName(data.data.name);
        setTokensInCustomCollection(data.data.tokens);
        infoObtained += 1;
        if (infoObtained === 2) {
          remove_loading();
        }
      });
    }
  };


  React.useEffect(() => {
    getData();
  }, []);

  const saveCollection = () => {
    add_tokens_to_collection_api(collectionId, collectionName, tokensInCustomCollection, (data) => {
      if (collectionId == null) {
        localStorage.setItem('selectedApiCollection', selectedCollection);
        window.location.href = '/collections/' + data.id;
      } else {
        Swal.fire({
          title: 'Changes saved!',
          text: "",
          icon: 'success',
          timer: 1000,
        });
      }
    }, (errors_data) => {
      if (errors_data.show_errors) {
        Swal.fire({
          title: 'An error occured',
          text: errors_data['errors'][0],
          icon: 'warning',
          timer: 1500,
        });
      }
    })
  }

  const changeCollectionsSelect = (collectionId, ev) => {
    const previousValue = selectedCollection;
    setSelectedCollection(collectionId);
    add_loading(window.document.body);
    setDisplayDraggableDiv(false);
    get_all_external_api_tokens(collectionId, (data) => {
      setTokenList(data.tokens);
      setDisplayDraggableDiv(true);
      remove_loading();
    }, () => {
      setSelectedCollection(previousValue);
      setDisplayDraggableDiv(true);
      remove_loading();
      Swal.fire({
        title: "An error occured while trying to get tokens from collection '" +
          allApiCollections.filter(c => c.collectionId === collectionId)[0].name + "'",
        text: "Try again or report.",
        icon: 'error',
        timer: 4000,
      });
    });
  }

  const appendTokenFunction = (token) => {
    var newTokensInCustomCollection = [...tokensInCustomCollection];
    newTokensInCustomCollection.push(token);
    setTokensInCustomCollection(newTokensInCustomCollection);
    setTimeout(
      () => document.getElementById('tokensInCustomCollectionContainer').scrollTop = document.getElementById('tokensInCustomCollectionContainer').scrollHeight,
      100
    );
  }

  const removeTokenFromCollection = (tokenId) => {
    var newTokensInCustomCollection = tokensInCustomCollection.filter(tokenInCollection => tokenInCollection.tokenId !== tokenId);
    setTokensInCustomCollection(newTokensInCustomCollection);
  }

  const isAdminBool = userInfo && userInfo.is_admin ? true : false;

  return (
    <div>
      <UserHeader loggedInUsername={loggedInUsername} setLoggedInUsername={setLoggedInUsername} redirectWhenLoggedOut={true}
        is_admin={isAdminBool}
        pageLanguage={pageLanguage} setPageLanguage={(lang) => { setLocalStorageLanguage(lang); setPageLanguage(lang); }}
        tickets_count={userInfo != null ? userInfo.tickets_count : 0}
        is_client_admin={userInfo != null ? userInfo.is_client_admin : false}
      />

      <div className='container_div' style={{ display: 'flex' }}>
        <label>Drag & Drop tokens' images to the right or double-click them, insert a title and save your collection.</label>
      </div>
      <div className='container_div' style={{ display: 'flex' }}>
        <div id="dropdownAndTokensDiv">

          <select value={selectedCollection}
            onChange={(e) => changeCollectionsSelect(e.target.value, e)}
            className='header-div'>
            {
              allApiCollections.map((apiCollection, idx) => <option key={idx} value={apiCollection.collectionId}>
                {apiCollection.name}
              </option>)
            }
          </select>
          <div id="draggableComponents" style={{ display: displayDraggableDiv ? 'block' : 'none' }}>
            {
              tokenList.filter(
                tokenObject => !tokensInCustomCollection.map(tokenInCollection => tokenInCollection.tokenId).includes(tokenObject.token.tokenId)
              ).map((token, idx) => <div key={idx}>
                <TokenDraggableComponent
                  onDoubleClick={appendTokenFunction} token={token.token}>
                </TokenDraggableComponent>
              </div>)
            }
          </div>

        </div>
        <div id="collectionRightDiv">
          <div id="nameAndButtonHeader" className='header-div'>
            <input type="text"
              value={collectionName} onChange={(e) => { setCollectionName(e.target.value) }}
              placeholder="" />
            <button className={"btn btn-secondary "}
              disabled={collectionName === "" || tokensInCustomCollection.length === 0}
              style={{ backgroundColor: "#434575", borderColor: "#434575" }}
              onClick={saveCollection}
              tooltip="asdasdas"
            >Save</button>
          </div>
          <div id="tokensInCustomCollectionContainer"
            onDrop={(ev) => utilDropFunction(ev, appendTokenFunction)} onDragOver={utilOnDragOver}
          >
            {tokensInCustomCollection.map((token, idx) => <div key={idx}>
              <TokenSquareComponent
                token={token}
                removeTokenFromCollection={removeTokenFromCollection}
              ></TokenSquareComponent>
            </div>)}
          </div>
        </div>
      </div>
    </div >
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
