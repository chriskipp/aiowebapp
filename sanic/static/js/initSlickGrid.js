function initSlickGrid(jsonData, containerid, draggableGrouping=true) {
      var options;
      var draggableGrouping;
      var gridMenuControl;
      var columns;
      var data;
      var draggableEnabled = draggableGrouping;
      var grid;

      var gridObjects = new Object();

      var gridData = object2Array(jsonData);

      $('#' + containerid)[0].outerHTML = "<div id='" + containerid + "'><div id='" + containerid + "-grid'></div></div>";

      function enumerate(arr) {
        for (i=0; i<arr.length;i++) {
          arr[i]['id'] = i;
        }
        return arr;
      };

      function toTitleCase(s) {
        return s[0].toUpperCase() + s.replace('_', ' ').slice(1)
      }

      function key2Column(k) {
        o = new Object({
                id: k,
                name: toTitleCase(k),
                field: k,
                sortable: true,
                resizable: true,
                selectable: true,
                focusable: true
        })
        return o
      }

      function array2Columns(arr) {
        var s = new Set();
        arr.forEach(function(element) {
          var ks = Object.keys(element);
          ks.map(e => s.add(e));
        });
        arr2 = new Array();
        s.forEach(k => arr2.push(key2Column(k)))
        return arr2
      }

      function object2Array(j) {
        var a;
        var keys = Object.keys(j);
        if (keys.includes('results')) {
          a = j['results'];
        } else if (Array.isArray(j)) {
          a = j;
        } else if (keys.length == 1) {
          a = j[keys[0]];
        } else {
          var c = new Array();
          a = new Array();
          for (k of keys.entries()) {
            if (Array.isArray(j[k[1]])) {
              var b = j[k[1]];
              b.forEach(function(e) {
                e['key'] = k[1];
              });
              c.push(b);
            }
          }
          for (i=0; i<c.length; i++) {
            var b = c[i];
            a = a.concat(b);
          }
        }
        a = enumerate(a);
        var columns = array2Columns(a);
        console.log(columns);
        return new Object({columns: columns, data: a})
      }

      function getGrouping(e) {
	var grouping = {
          getter: e['id'],
          formatter: function (g) { 
            return e['name'] + ': <b>' + g.value + '</b> (' + g.count + ') items'
          },
          aggregators: [
	    new Slick.Data.Aggregators.Avg('id')
	  ],
          aggregateCollapsed: false,
          aggregateChildGroups: false,
          aggregateEmpty: true,
          collapsed: true,
          lazyTotalsCalculation: false
	}
	return grouping
      }

      function isDefOrSet(e, key, alt) {
        if (e[key] == undefined) {
          e[key] = alt;
        }
        return e
      }

      var columnAutosizeDefaults = {
  	autoSize: {
          ignoreHeaderText: false,
          autosizeColsMode: Slick.ColAutosizeMode.ContentIntelligent,
          rowSelectionMode: Slick.RowSelectionMode.FirstNRow,
	  rowSelectionCount: 100,
          valueFilterMode: Slick.ValueFilterMode.GetLongestTextAndSub,
          widthEvalMode: Slick.WidthEvalMode.CanvasTextSize,
        }
      };
      

      function initCols(cols) {
	cols.forEach(function(e) {
	  if (typeof(e) != "object") {
	    e = new Object({
	      'id': e,
	      'field': e,
	      'name': toTitleCase(e)
	    });
	  } else {
	    var k = Object.keys(e);
	    if (k.includes('id')) {
              e = isDefOrSet(e, 'field', e['id']);
              e = isDefOrSet(e, 'name', toTitleCase(e['id']));
	    } else if (k.includes('field')) {
	      e = isDefOrSet(e, 'id', e['field']);
	      e = isDefOrSet(e, 'name', toTitleCase(e['field']));
	    } else if (k.includes('name')) {
	      e = isDefOrSet(e, 'id', toLowerCase(e['name']));
	      e = isDefOrSet(e, 'field', toLowerCase(e['name']));
            }
	  }
	  e = isDefOrSet(e, 'sortable', true),
	  e = isDefOrSet(e, 'focusable', true),
	  e = isDefOrSet(e, 'selectable', true),
	  e = isDefOrSet(e, 'rerenderOnResize', true),
	  e = isDefOrSet(e, 'header', headermenu),
	  e = isDefOrSet(e, 'groupTotalsFormatter', e.sumTotalsFormatter),
	  e = isDefOrSet(e, 'grouping', getGrouping(e));

	  e = isDefOrSet(e, 'minWidth', 30);
	  e = isDefOrSet(e, 'maxWidth', 500);

	  e['autosize'] = columnAutosizeDefaults['autosize'];
        });
	return cols
      }

      gridData = object2Array(jsonData);
      columns = gridData['columns'];
      data = gridData['data'];

      var headermenu = {
        menu: {
          items: [
            {
	      iconImage: "/static/images/sort-up.svg",
              title: "Sort Ascending",
              tooltip: "Sort ascending by this column",
              command: "sort-asc"
            },
            {
	      iconImage: "/static/images/sort-down.svg",
              title: "Sort Descending",
              tooltip: "Sort descending by this column",
              command: "sort-desc"
            },
            {
	      iconImage: "/static/images/eye-slash.svg",
              title: "Hide Column",
              command: "hide",
              tooltip: "Hide this column"
            },
            {
              divider: true,
              command: ""
            },
            {
              iconCssClass: "icon-help",
              title: "Help",
              command: "help"
            }
          ]
        }
      };

      // MetadataProvider
      var groupItemMetadataProvider = new Slick.Data.GroupItemMetadataProvider();
      var dataView = new Slick.Data.DataView({
        groupItemMetadataProvider: groupItemMetadataProvider,
        inlineFilters: true
      });
      
      // DraggableGrouping
      if (draggableGrouping == true) {
        var draggableGrouping = new Slick.DraggableGrouping(
          {
            iconImage : "/static/images/times-circle.svg",
	    groupIconImage: "/static/images/plus-circle.svg",
		dropPlaceHolderText: '<span style="align-self:center;margin:0px;padding:0;"><i class="fas fa-parachute-box"> </i> Drop columns here...</span>'
          }
        );
      };

      options = {
	editable: true,
	autoEdit: false,
	autoHeight: false,
        enableCellNavigation: true,
        enableColumnReorder: true,
        enableAutoSizeColumns: true,
	autosizeColsMode: Slick.GridAutosizeColsMode.FitColsToViewport,
  	autosizeColPaddingPx: 4,
  	autosizeTextAvgToMWidthRatio: 0.75,
	viewportSwitchToScrollModeWidthPercent: 120,
	enableTextSelectionOnCells: false,
	fullWidthRows: true,
	forceFitColumns: false,
	multiSelect: true,
	multiColumnSort: true,
	numberedMultiColumnSort: true,
	sowHeaderRow: false,
	sortColNumberInSeparatorSpan:  false,
	syncColumnCellResize: true,
        createPreHeaderPanel: false,
        showPreHeaderPanel: false,
        preHeaderPanelHeight: 0,
        gridMenu: {
          customTitle: "GridMenu",
          columnTitle: "Columns",
          hideForceFitButton: false,
          hideSyncResizeButton: false,
	  iconImage: "/static/images/bars.svg",
          leaveOpen: false,
          menuWidth: 20,
          resizeOnShowHeaderRow: true,
          customItems: [
            {
              title: "Toggle Top Panel",
              disabled: false,
              command: "toggle-toppanel"
            },
            {
              title: "Toggle Fit Columns",
              disabled: false,
              command: "toggle-forceFit"
            },
            {
              title: "Autosize Columns",
              disabled: false,
              command: "toggle-autoSizeColumns"
            },
            {
              title: "Full Width Rows",
              disabled: false,
              command: "toggle-fullWidthRows"
            },
            {
              title: "Set Cell Selection",
              disabled: false,
              command: "set-cell-selection"
            },
            {
              title: "Set Row Selection",
              disabled: false,
              command: "set-row-selection"
            },
            {
              title: "Set Fit Columns To Viewport",
              disabled: false,
              command: "set-fit-cols-to-viewport"
            },
            {
              title: "Set Ignore Viewport Width",
              disabled: false,
              command: "set-ignore-viewport-width"
            },
            {
              divider: true,
              command: ""
            },
            {
              iconImage: "",
              title: "Disabled Command",
              disabled: true,
              command: "custom-command"
            }
          ]
        }
      };

      if (draggableGrouping != false) {
	options['enableColumnReorder'] = draggableGrouping.getSetupColumnReorder;
        options['showPreHeaderPanel'] = true;
        options['createPreHeaderPanel'] = true;
        options['preHeaderPanelHeight'] = 25;
      }

      grid = new Slick.Grid('#' + containerid + '-grid', dataView, initCols(columns), options);

      grid.registerPlugin(groupItemMetadataProvider);

      if (draggableGrouping != false) {
        grid.registerPlugin(draggableGrouping);
      }

      function clearGroupings() {
         draggableGrouping.clearDroppedGroups();
      }
      
      function toggleDraggableGrouping() {
         clearGroupings();
        if ( draggableEnabled == true ) {
          grid.setPreHeaderPanelVisibility(false);
          draggableEnabled = false;
        } else {
          grid.setPreHeaderPanelVisibility(true);
          draggableEnabled = true;
        }
      }
      
      function toggleGrouping(expand) {
        if(expand) {
          dataView.expandAllGroups();
          $(".slick-group-toggle-all").removeClass('collapsed').addClass('expanded');
        } else {
          dataView.collapseAllGroups();
          $(".slick-group-toggle-all").removeClass('expanded').addClass('collapsed');
        }
      }

      // Make the grid respond to DataView change events.
      dataView.onRowCountChanged.subscribe(function (e, args) {
        grid.updateRowCount();
        grid.render();
      });

      dataView.onRowsChanged.subscribe(function (e, args) {
        grid.invalidateRows(args.rows);
        grid.render();
      });

      // Handle Sort Events
      grid.onSort.subscribe(function(e, args) {
        var comparer = function(a, b) {
      	if (a[args.sortCols[0].sortCol.field] == undefined) {
          return 1;
      	} else if (b[args.sortCols[0].sortCol.field] == undefined) {
          return -1;
      	} else {
          return (a[args.sortCols[0].sortCol.field] > b[args.sortCols[0].sortCol.field]) ? 1 : -1;
        }
        };
        dataView.sort(comparer, args.sortCols[0].sortAsc);
      });
    
      // Plugins

      // Resizer Plugin
      var resizer;
      function resumeAutoResize() {
        resizer.pauseResizer(false);
        resizer.resizeGrid();
      }
    
      resizer = new Slick.Plugins.Resizer({
        container: '#' + containerid,
    
        // optionally define some padding and dimensions
        rightPadding: 0,
        bottomPadding: 0,
        minHeight: 150,
        minWidth: 250,
    
      });

      resumeAutoResize();

      grid.registerPlugin(resizer);

      gridObjects['resizer'] = resizer;

      grid.registerPlugin(new Slick.AutoTooltips({ enableForHeaderCells: true, enableForCells: true }));

      // Initiate and set Selection Models
      var rowSelectionModel = new Slick.RowSelectionModel();
      var cellSelectionModel = new Slick.CellSelectionModel();
      gridObjects['selectionModels'] = {
	rowSelectionModel: rowSelectionModel,
	cellSelectionModel: cellSelectionModel
      }
      grid.setSelectionModel(cellSelectionModel);

      // Synchonize DataView- and Grid Selection
      function syncGridSelection(grid, preserveHidden) {
          var self = this;
          var selectedRowIds = self.mapRowsToIds(grid.getSelectedRows());;
          var inHandler;
        
          function update() {
              if (selectedRowIds.length > 0) {
                  inHandler = true;
                  var selectedRows = self.mapIdsToRows(selectedRowIds);
                  if (!preserveHidden) {
                      selectedRowIds = self.mapRowsToIds(selectedRows);
                  }
                  grid.setSelectedRows(selectedRows);
                  inHandler = false;
              }
          }
        
          grid.onSelectedRowsChanged.subscribe(function(e, args) {
              if (inHandler) { return; }
              selectedRowIds = self.mapRowsToIds(grid.getSelectedRows());
          });
          this.onRowsChanged.subscribe(update);
          this.onRowCountChanged.subscribe(update);
      }
          
      // Initiate and register HeaderMenu 
      var headerMenuPlugin = new Slick.Plugins.HeaderMenu({});
      grid.registerPlugin(headerMenuPlugin);

      // Functions serving Slickgrid funcionality
      var removeColumnById = function(array, idVal) {
        return array.filter(function (el, i) {
          return el.id !== idVal;
        });
      };

      var removeSortColumnById = function(array, idVal) {
        return array.filter(function (el, i) {
          return el.columnId !== idVal;
        });
      };

      function autoAlignMenu(isEnabled) {
        headerMenuPlugin.setOptions({ autoAlign: isEnabled });
      }

      // Define HeaderMenu Commands 
      headerMenuPlugin.onCommand.subscribe(function(e, args) {
        if(args.command === "hide") {
          // hide column
          selectedColumns = removeColumnById(selectedColumns, args.column.id);
          grid.setColumns(selectedColumns);

        } else if (args.command === "sort-asc" || args.command === "sort-desc") {
          // sort column asc or desc
          var isSortAsc = (args.command === "sort-asc");
      
          var sortCols = removeSortColumnById(grid.getSortColumns(), args.column);
          sortCols.unshift(args.column);
	  console.log(sortCols);
          grid.setSortColumns(sortCols);
          
      	  var comparerAsc = function(a, b) {
      	    if (a[sortCols[0].field] == undefined) {
              return 1;
      	    } else if (b[sortCols[0].field] == undefined) {
              return -1;
      	    } else {
              return (a[sortCols[0].field] > b[sortCols[0].field]) ? 1 : -1;
      	    }
      	  };

      	  var comparerDesc = function(a, b) {
      	    if (a[sortCols[0].field] == undefined) {
              return -1;
      	    } else if (b[sortCols[0].field] == undefined) {
              return 1;
      	    } else {
              return (a[sortCols[0].field] < b[sortCols[0].field]) ? 1 : -1;
      	    }
      	  };

	  if (isSortAsc == true) {
            dataView.sort(comparerAsc, sortCols[0]);
	  } else {
            dataView.sort(comparerDesc, sortCols[0]);
	  };
        } else {
          // command not recognised
          alert("Command: " + args.command);
        }
      });

      // GridMenuControl
      gridMenuControl = new Slick.Controls.GridMenu(columns, grid, options);

      // subscribe to Grid Menu event(s)
      gridMenuControl.onCommand.subscribe(function(e, args) {
        if (args.command === "toggle-toppanel") {
          grid.setTopPanelVisibility(!grid.getOptions().showTopPanel);
        } else if (args.command === "toggle-forceFit") {
          grid.setOptions({
            forceFitColumns: !grid.getOptions()['forceFitColumns']
          })
        } else if (args.command === "toggle-fullWidthRows") {
          grid.setOptions({
            fullWidthRows: !grid.getOptions()['fullWidthRows']
          })
        } else if (args.command === "toggle-autoSizeColumns") {
          grid.setOptions({
            enableAutoSizeColumns: !grid.getOptions()['enableAutoSizeColumns']
          })
        } else if (args.command === "set-cell-selection") {
          grid.setSelectionModel(
	    gridObjects['selectionModels']['cellSelectionModel']
	  );
        } else if (args.command === "set-row-selection") {
          grid.setSelectionModel(
	    gridObjects['selectionModels']['rowSelectionModel']
	  );
        } else if (args.command === "set-fit-cols-to-viewport") {
	  grid.setOptions({
            autosizeColsMode: Slick.GridAutosizeColsMode.LegacyForceFit
          });
        } else if (args.command === "set-ignore-viewport-width") {
	  grid.setOptions({
            autosizeColsMode: Slick.GridAutosizeColsMode.IgnoreViewport
          });
        } else {
          alert("Command: " + args.command);
        }
      });
           
      // subscribe to event when column visibility is changed via the menu
      gridMenuControl.onColumnsChanged.subscribe(function(e, args) {
        console.log('Columns changed via the menu');
         selectedColumns = grid.getColumns(); 
         grid.autosizeColumns();
      });
      
      // subscribe to event when menu is closing
      gridMenuControl.onMenuClose.subscribe(function(e, args) {
        console.log('Menu is closing');
        grid.autosizeColumns();
      });
      
      // Set Data
      dataView.setItems(data);

      var containerNode = grid.getContainerNode();
      function correctNoHeaderPanel(containerNode) {
        let s = '#' + containerNode.id;
        $(s + ' .slick-pane-header.slick-pane-left')[0].style.height = '36px';
        $(s + ' .slick-gridmenu-button')[0].style.top = '4px';
        $(s + ' .slick-pane.slick-pane-top.slick-pane-left')[0].style.top = '36px';
      }
      
      if (draggableGrouping == false) {
	correctNoHeaderPanel(containerNode);
      }

      grid.autosizeColumns();

      return new Object({
	      grid: grid,
	      dataView: dataView,
	      columns: initCols(columns),
	      gridObjects: gridObjects
      })
}
