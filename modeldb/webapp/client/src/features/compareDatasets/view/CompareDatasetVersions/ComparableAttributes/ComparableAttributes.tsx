import * as React from 'react';

import ClientSuggestion from 'shared/view/domain/ModelRecord/ModelRecordProps/shared/ClientSuggestion/ClientSuggestion';
import { IAttribute } from 'shared/models/Attribute';
import ScrollableContainer from 'shared/view/elements/ScrollableContainer/ScrollableContainer';

import ComparableAttributeButton from './ComparableAttributeButton/ComparableAttributeButton';
import styles from './ComparableAttributes.module.css';
import { IAttributesDiffInfo, DatasetVerisonEntityType } from 'features/compareDatasets/store/compareDatasets';

interface ILocalProps {
  entity1Attributes: IAttribute[];
  entity2Attributes: IAttribute[];
  entityType: DatasetVerisonEntityType;
  diffInfo: IAttributesDiffInfo;
  docLink?: string;
}

export interface IComparedAttribute {
  attribute: IAttribute;
  otherEntityAttribute?: IAttribute;
  diffInfo: IAttributesDiffInfo[string];
}

class ComparableAttributes extends React.PureComponent<ILocalProps> {
  public render() {
    const {
      entity1Attributes,
      entity2Attributes,
      diffInfo,
      entityType,
      docLink,
    } = this.props;

    const comparedAttributes = (() => {
      if (entityType === DatasetVerisonEntityType.entity1) {
        return entity1Attributes.map<IComparedAttribute>(attribute => ({
          attribute,
          otherEntityAttribute: entity2Attributes.find(
            attribute2 => attribute.key === attribute2.key
          ),
          diffInfo: diffInfo[attribute.key],
        }));
      }
      return entity2Attributes.map<IComparedAttribute>(attribute => ({
        attribute,
        otherEntityAttribute: entity1Attributes.find(
          attribute1 => attribute.key === attribute1.key
        ),
        diffInfo: diffInfo[attribute.key],
      }));
    })();

    return (
      <div className={styles.root} data-test="attributes">
        {comparedAttributes.length !== 0 ? (
          <ScrollableContainer
            maxHeight={180}
            minRowCount={5}
            elementRowCount={comparedAttributes.length}
            containerOffsetValue={12}
            children={
              <>
                {comparedAttributes.map(comparedAttribute => (
                  <ComparableAttributeButton
                    key={comparedAttribute.attribute.key}
                    comparedAttribute={comparedAttribute}
                    entityType={entityType}
                  />
                ))}
              </>
            }
          />
        ) : (
          docLink && (
            <ClientSuggestion
              fieldName={'attribute'}
              clientMethod={'log_attribute()'}
              link={docLink}
            />
          )
        )}
      </div>
    );
  }
}

export default ComparableAttributes;
