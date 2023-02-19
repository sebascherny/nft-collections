'use strict';
const e = React.createElement;


function App() {
  const [allCollections, setAllCollections] = React.useState([]);
  const [loggedInUsername, setLoggedInUsername] = React.useState(null);
  const [pageLanguage, setPageLanguage] = React.useState("en");
  const [userInfo, setUserInfo] = React.useState(null);

  const success = (data) => {
    setAllCollections(data.data.collections);
  };

  const getData = () => {
    add_loading(window.document.body);
    getLoggedInUsername((username) => { setLoggedInUsername(username) });
    getPageLanguage((lang => { setPageLanguage(lang); }));
    get_user_data_api((data) => setUserInfo(data.data))
    get_all_collections_api((data) => {
      success(data);
      remove_loading();
    }, (text) => { console.log("Error: ", text) });
  };

  React.useEffect(() => {
    getData();
  }, []);

  const deleteCollection = (collectionId) => {
    Swal.fire({
      title: 'Are you sure?',
      text: "This action cannot be undone",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#FBB142',
      cancelButtonColor: '#434575',
      confirmButtonText: 'Yes, delete'
    }).then((result) => {
      if (result.isConfirmed) {
        delete_collection_api(collectionId, () => {
          Swal.fire({
            title: 'Deleted!',
            text: "",
            icon: 'success',
            timer: 1000,
          });
          getData();
        });
      }
    });
  };

  const isAdminBool = userInfo != null && userInfo.is_admin ? true : false;

  return (
    <div>
      <UserHeader
        loggedInUsername={loggedInUsername} setLoggedInUsername={setLoggedInUsername}
        redirectWhenLoggedOut={true}
        viewName="datasets"
        pageLanguage={pageLanguage} setPageLanguage={(lang) => { setLocalStorageLanguage(lang); setPageLanguage(lang); }}
        is_admin={isAdminBool}
        is_client_admin={userInfo != null ? userInfo.is_client_admin : false}
      />
      <div className='container_div'>
        {userInfo != null ?
          <div>
            {
              allCollections.length > 0 ?
                <h2 style={{ marginBottom: '30px' }}>Custom Collections</h2> :
                <h2 style={{ marginBottom: '30px' }}>
                  <a className={"btn btn-secondary "}
                    style={{ backgroundColor: "#434575", borderColor: "#434575" }}
                    href="/new-collection">Create First Collection</a></h2>
            }
            <div style={{ overflow: 'scroll', height: '500px' }}>
              <div style={{ overflowY: 'hidden' }}>
                {allCollections.map((row) =>
                  <div key={row.id}
                    style={{
                      display: 'flex', width: '100%',
                      padding: '10px', marginBottom: '20px',
                      border: '2px solid black'
                    }}>
                    <div style={{ width: '55%' }}>
                      <h4 style={{ overflowWrap: 'break-word' }}>{row.name}</h4>
                      <label>{row.token_count} item{row.token_count > 1 ? "s" : ""}</label>
                    </div>
                    <a className="btn btn-hover"
                      style={{
                        border: "solid 1px", width: "20%",
                        height: "40px", marginTop: '10px',
                        marginLeft: '2%', marginRight: '2%'
                      }}
                      onClick={() => { deleteCollection(row.id) }}>Delete</a>
                    <a className="btn btn-dark"
                      style={{
                        marginLeft: "10px", border: "solid 1px", width: "20%",
                        height: "40px", marginTop: '10px'
                      }}
                      href={"/collections/" + row.id}>Edit</a>
                  </div>
                )}
              </div>
            </div>
            <br />
          </div> : null
        }
      </div>
    </div>
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
