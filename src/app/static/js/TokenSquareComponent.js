'use strict';

class TokenSquareComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={{
                height: '100%',
                border: '1px solid black',
                padding: '5px 5px 5px 5px'
            }}>
                <button
                    className="btn-danger"
                    style={{ marginBottom: '10px', width: '30px' }}
                    onClick={() => this.props.removeTokenFromCollection(this.props.token.tokenId)}
                >X</button>
                <div style={{ textAlign: 'center' }}>
                    <img
                        id={"draggableImg_" + this.props.token.tokenId}
                        style={{ width: '80%' }}
                        src={this.props.token.image}
                        draggable={false}
                    ></img>
                </div>
                <label
                    style={{ width: '100%', verticalAlign: 'middle', fontWeight: 'normal' }}
                >{this.props.token.name || "#" + this.props.token.tokenId}</label>
            </div>
        );
    }
};