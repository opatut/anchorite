import React from 'react';
import classnames from 'classnames';
import {BaseComponent} from '../BaseComponent';

import Item from './Item';
import HoverButton from './HoverButton';
import {find} from '../data';

export default class Shelf extends BaseComponent {
	static contextTypes = {
		dispatch: React.PropTypes.func.isRequired,
		types: React.PropTypes.object.isRequired,
	}

	render() {
		const {onStageItem, inventory, className} = this.props;
		const {dispatch} = this.context;

		const onClick = item_type_id => event => {
			event.preventDefault();

			dispatch({
				type: 'stage.add',
				item_type_id,
				count: 1,
			});
		}

		return <div className={classnames('shelf', className)}>
			{inventory.map(({item_type_id, count}, i) => {
				const itemType = find(this.context.types.item_types, item_type_id);
				return <HoverButton color='green' icon='+' onClick={onClick(item_type_id)} key={item_type_id} title={itemType.name}>
					<Item itemType={itemType} count={count} />
				</HoverButton>;
			})}
		</div>;
	}
}
