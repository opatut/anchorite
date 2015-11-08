import React from 'react';
import {isEqual} from 'lodash';

export class BaseComponent extends React.Component {
	shouldComponentUpdate(nextProps, nextState) {
		return !isEqual(nextState, this.state) || !isEqual(nextProps, this.props);
	}
}
export default BaseComponent;
