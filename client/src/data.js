import * as lodash from 'lodash';

export function find(items, id, key='id') {
	return lodash.find(items, (item) => {
		return item[key] === id;
	});
}

export class Inventory {
	constructor(contents = {}) {
		if (Array.isArray(contents)) {
			this.contents = lodash.transform(contents, (acc, item) => {
				acc[item.item_type_id] = (acc[item.item_type_id] || 0) + item.count;
			} , {});
		} else {
			this.contents = contents;
		}
	}

	toArray() {
		return Object.keys(this.contents).sort().map((key) => {
			return { item_type_id: parseInt(key), count: this.contents[key] };
		});
	}

	toString() {
		return this.toArray().map(({item_type_id, count}) => `${item_type_id}:${count}`).join('|');
	}

	map(...args) {
		return this.toArray().map(...args);
	}

	equals(other) {
		if (!other) return false;
		return lodash.isEqual(this.contents, other.contents);
	}

	subtract(other) {
		if (!other) return this;

		const result = lodash.clone(this.contents);

		for (let key in other.contents) {
			if (!result[key]) {
				throw new Error('Negative inventory count');
			}

			result[key] = result[key] - other.contents[key];

			if (result[key] < 0) {
				throw new Error('Negative inventory count');
			} else if (result[key] == 0) {
				delete result[key];
			}
		}

		return new Inventory(result);
	}

	add(right) {
		const result = lodash.clone(this.contents);

		for (let key in right.contents) {
			result[key] = (result[key] || 0) + right.contents[key];
		}

		return new Inventory(result);
	}

}

