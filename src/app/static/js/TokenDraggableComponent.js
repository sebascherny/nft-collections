'use strict';

class TokenDraggableComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (
            this.props.token.image != null ?
                <div id={"draggableDiv_" + this.props.token.tokenId}
                    style={{ maxWidth: '100%', marginBottom: '10px' }}
                >
                    <img
                        id={"draggableImg_" + this.props.token.tokenId}
                        style={{ width: '40%', marginRight: '5px' }}
                        src={this.props.token.image}
                        draggable={true}
                        onDragStart={(ev) => utilDragStartFunction(ev, this.props.token)}
                        onDoubleClick={() => this.props.onDoubleClick(this.props.token)}
                    ></img>
                    <label
                        style={{ width: '50%', verticalAlign: 'middle' }}
                    >{this.props.token.name || "#" + this.props.token.tokenId}</label>
                </div> :
                null
        );
    }
};
