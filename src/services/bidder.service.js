const Bidder = require('../models/bidder.schema');
const { sendOtpByEmail, sendOtpBySms } = require('./auth.service');
const verifyGstin = require('./verification.service');

const bidderList = async (searchText, pageNo, pageSize) => {
    let result;
    let bidders;
    const queryObj = { isDeleted: false };

    let aggregationPipeline = [];
    let searchObj;
    let skip, limit;

    if (searchText && searchText !== 'undefined') {
        searchObj = {
            'index': 'bidder',
            'text': {
                'query': searchText,
                'path': ['companyName', 'preferenceCategory', 'registeredAddress', 'partners', 'bidderType', 'city', 'state', 'country', 'panNumber', 'gstinNumber', 'establishmentYear', 'natureOfBusiness', 'legalStatus', 'companyCategory', 'contactName']
            }
        };

        aggregationPipeline.push({ $search: searchObj });
    }

    aggregationPipeline.push({ $match: queryObj });

    if (pageNo && pageSize) {
        if (pageNo < 1 || pageSize < 1) {
            limit = pageSize;
            skip = ((pageNo - 1) * pageSize);
            aggregationPipeline.push({ $skip: skip });
            aggregationPipeline.push({ $limit: limit });
        }
    }

    bidders = await Bidder.aggregate(aggregationPipeline).collation({ locale: 'en_US' });

    result = {
        message: 'Bidder List',
        data: {
            bidders
        }
    };
    return result;
}

const bidderById = async (req) => {
    let result;

    const bidder = await Bidder.findById(req.params.id);

    result = {
        message: 'Bidder details',
        data: {
            bidder
        }
    };
    return result;
}

const bidderCreate = async (req) => {
    let result;
    const newBidder = new Bidder(req.body);
    
    let information = true;
    const panVerification = 1;
    const gstinVerfication = await verifyGstin(newBidder.gstinNumber);

    if (!panVerification) {
        result = {
            message: 'Enter correct PAN',
            error: true
        }
        information = false;
    }
    if (!gstinVerfication) {
        result = {
            message: 'Enter correct GSTIN',
            error: true
        }
        information = false;
    }
    if (!panVerification && !gstinVerfication) {
        result = {
            message: 'Enter correct PAN & GSTIN',
            error: true
        }
        information = false;
    }
    if (!information) {
        return result;
    }

    await newBidder.save(req);

    const authEmailId = await sendOtpByEmail(req, newBidder);
    const authSmsId = await sendOtpBySms(req, newBidder);

    result = {
        message: 'Bidder successfully created',
        data: { 
            authEmailId,
            authSmsId,
            newBidder
        }
    };
    return result;
};

const bidderUpdate = async (req) => {
    let result;

    const bidder = await Bidder.findByIdAndUpdate(req.params.id, req.body);

    result = {
        message: 'Bidder updated successfully',
        data: bidder
    };
    return result;
};

const bidderDelete = async (req) => {
    let result;

    const bidder = await Bidder.findByIdAndUpdate(req.params.id, { isDeleted: true });

    result = {
        message: 'Bidder deleted successfully',
        data: bidder
    };
    return result;
};

module.exports = {
    bidderList,
    bidderById,
    bidderCreate,
    bidderUpdate,
    bidderDelete
};