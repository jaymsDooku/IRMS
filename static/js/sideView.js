var sideView = (function(sideViewConfig) {

	var m = { };
	var mainSection = sideViewConfig.mainSection;

	m.currentSideView = null;

	m.open = function(sideView) {
		if (m.currentSideView != null) {
        	m.close(m.currentSideView);
	    }

	    var closeViewBtns = sideView.getElementsByClassName('close-view-btn');
	    domUtil.onClick(closeViewBtns, function(event) {
	    	m.close();
	    });

	    m.currentSideView = sideView;

	    m.currentSideView.style.width = sideViewConfig.width;
	    m.currentSideView.style.paddingLeft = sideViewConfig.padding;
	    mainSection.style.marginRight = sideViewConfig.width;
	}

	m.close = function() {
		if (m.currentSideView == null) {
			return;
		}

		m.currentSideView.style.width = "0";
	    m.currentSideView.style.paddingLeft = "0";
	    mainSection.style.marginRight = "0";

	    m.currentSideView = null;
	}

	return m;
})({ mainSection: document.getElementsByClassName('container')[0], 
		width: "250px", 
		padding: "15px" });