class PushButtonSelectorCard extends HTMLElement {
    set hass(hass) {
      const entityId = this.config.entity;
      const entity = hass.states[entityId];
      const options = entity.attributes.options;
      const selectedOption = entity.state;
      const secondaryInfo = this._renderTemplate(entity.attributes.secondary_info);
      const activeStyle = this.config.style?.active || {};
      const inactiveStyle = this.config.style?.inactive || {};
  
      this.innerHTML = `
        <ha-card>
          <div class="entity-info">
            ${this.config.icon ? `<ha-icon icon="${this._renderTemplate(this.config.icon)}"></ha-icon>` : ''}
            <span>${this.config.name || ''}</span>
            <span>${secondaryInfo || ''}</span>
          </div>
          <div class="button-row">
            ${options.map(option => `
              <button
                class="button ${option === selectedOption ? 'active' : ''}"
                @click="${() => this._handleTap(hass, entityId, option)}"
                style="${option === selectedOption ? this._styleString(activeStyle) : this._styleString(inactiveStyle)}"
              >
                <ha-icon icon="${this._renderTemplate(this.config.icons?.[option] || 'mdi:help-circle')}"></ha-icon>
              </button>
            `).join('')}
          </div>
        </ha-card>
      `;
    }
  
    _renderTemplate(templateString) {
      if (!templateString) return '';
      const template = new Function('states', `return \`${templateString}\`;`);
      return template(this.hass.states);
    }
  
    _styleString(style) {
      return Object.entries(style).map(([key, value]) => `${key}: ${value};`).join(' ');
    }
  
    _handleTap(hass, entityId, option) {
      hass.callService('input_select', 'select_option', {
        entity_id: entityId,
        option: option
      });
    }
  
    setConfig(config) {
      if (!config.entity) {
        throw new Error('You need to define an entity');
      }
      this.config = config;
    }
  
    getCardSize() {
      return 1;
    }
  }
  
  customElements.define('push-button-selector-card', PushButtonSelectorCard);
  window.customCards = window.customCards || [];
  window.customCards.push({
    type: 'push-button-selector-card',
    name: 'Push Button Selector Card',
    preview: false,
    description: 'A configurable push-button selector card',
    editor: 'push-button-selector-card-editor',
  });

  class PushButtonSelectorCardEditor extends HTMLElement {
    setConfig(config) {
      this._config = config;
      this.render();
    }
  
    render() {
      this.innerHTML = `
        <div class="card-config">
          <paper-input
            label="Entity"
            value="${this._config.entity || ''}"
            config-value="entity"
          ></paper-input>
          <paper-input
            label="Name"
            value="${this._config.name || ''}"
            config-value="name"
          ></paper-input>
          <paper-input
            label="Icon"
            value="${this._config.icon || ''}"
            config-value="icon"
          ></paper-input>
          <ha-formfield label="Use Template for Icon?">
            <ha-switch
              .checked="${this._config.use_template_icon === true}"
              config-value="use_template_icon"
            ></ha-switch>
          </ha-formfield>
          <!-- Repeat for other options like color, actions, etc. -->
        </div>
      `;
  
      this.querySelectorAll('paper-input, ha-switch').forEach((element) => {
        element.addEventListener('change', (event) => this._valueChanged(event));
      });
    }
  
    _valueChanged(event) {
      if (!this._config) return;
  
      const target = event.target;
      if (this._config[target.getAttribute('config-value')] === target.value) return;
  
      const newConfig = {
        ...this._config,
        [target.getAttribute('config-value')]: target.checked !== undefined ? target.checked : target.value,
      };
  
      this.dispatchEvent(new CustomEvent('config-changed', { detail: { config: newConfig } }));
    }
  }
  
  customElements.define('push-button-selector-card-editor', PushButtonSelectorCardEditor);
  
  // Register the editor for the custom card
  window.customCards = window.customCards || [];
  window.customCards.push({
    type: 'push-button-selector-card',
    name: 'Push Button Selector Card',
    preview: false,
    description: 'Custom push button selector with multiple states and actions',
  });