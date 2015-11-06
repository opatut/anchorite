import React from 'react';

import * as items from '../resources/items';

export default class Item extends React.Component {
	render() {
		const {
			itemType,
			count,
		} = this.props;

		const {
			icon,
			name,
		} = itemType;

		return <div className='item'>
			<img src={items[icon]} />
			{ count && <div className='count'>{count}</div>}
		</div>;
	}
}
