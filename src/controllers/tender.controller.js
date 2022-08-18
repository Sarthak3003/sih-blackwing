const { tenderList, tenderById, tenderCreate, tenderUpdate, tenderDelete } = require('./../services/tender.service');

const createTender = async (req, res) => {
    try {
        let result = await tenderCreate(req);

        if (result.error) {
            res.status(400).json({ result });
            return;
        }

        res.status(201).json({ result });
    } catch (error) {
        res.status(400).json({
            result: {
                message: error.message
            }
        });
    }
};

const getTenderById = async (req, res) => {
    try {
        let result = await tenderById(req);

        res.status(200).json({ result });
    } catch (error) {
        res.status(400).json({
            result: {
                message: error.message
            }
        });
    }
}

const getTenderList = async (req, res) => {
    try {
        let result = await tenderList(req.query.searchText, req.headers.pageNo, req.headers.pageSize);

        res.status(200).json({ result });
    } catch (error) {
        res.status(400).json({
            result: {
                message: error.message
            }
        });
    }
};

const updateTender = async (req, res) => {
    try {
        let result = await tenderUpdate(req);

        res.status(200).json({ result });
    } catch (error) {
        res.status(400).json({
            result: {
                message: error.message
            }
        });
    }
};

const deleteTender = async (req, res) => {
    try {
        let result = await tenderDelete(req);

        res.status(200).json({ result });
    } catch (error) {
        res.status(400).json({
            result: {
                message: error.message
            }
        });
    }
};

module.exports = {
    createTender,
    getTenderById,
    getTenderList,
    updateTender,
    deleteTender
};